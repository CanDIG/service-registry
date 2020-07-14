# pylint: disable=invalid-name
# pylint: disable=C0301
"""
Implement endpoints of model service
"""
import sys
import uuid
from urllib.parse import urljoin
import requests
from service_registry import orm
from service_registry.orm import models
from service_registry.api.logging import apilog
from service_registry.api.models import Error, ServiceType
from service_registry.api.models import Service, ExternalService
from service_registry.orm.models import URL, Service as ORM_Service, Type, Organization
from tornado.options import options

SERVICE_NAME = "CINECA Service Registry"
THIS_SERVICE_TYPE = ServiceType(group='org.ga4gh', artifact='service-registry', version='1.0.0')
THIS_SERVICE = Service(id='this.service',
                       name='CINECA service registry',
                       type=THIS_SERVICE_TYPE,
                       description='CINECA service registry',
                       organization={'name': "CINECA", 'url': 'www.cineca-project.eu'},
                       version='1.0.0')


def get_service_info_and_active_status(url):
    """
    Fetch service info and active status of url
    """
    db_session = orm.get_session()
    active = True

    try:
        url_orm = db_session.query(URL).filter(URL.url == url).scalar()
    except orm.ORMException as e:
        print("Error connecting to database: " + str(e), file=sys.stderr, flush=True)
        return None, active

    service_orm = url_orm.service
    service_info_url = urljoin(f"{url}/", "service-info")
    print(f"[{SERVICE_NAME}] Contacting {service_info_url}", flush=True)
    try:
        r = requests.get(service_info_url, timeout=1)
        if r.status_code != 200:
            print(f"[{SERVICE_NAME}] Non-200 status code on {service_info_url}: {r.status_code}", file=sys.stderr,
                  flush=True)
            service_data = get_service_data_from_db(service_orm)
            active = False
        else:
            service_data = r.json()
    except requests.exceptions.Timeout:
        print(f"[{SERVICE_NAME}] Encountered timeout with {service_info_url}", file=sys.stderr, flush=True)
        service_data = get_service_data_from_db(service_orm)
        active = False

    if not service_data:
        return None, active

    # add the service to the database if it is not already in the database
    if not service_orm:
        service_type = Type(id=uuid.uuid4(), group=service_data['type']['group'],
                            artifact=service_data['type']['artifact'], version=service_data['type']['version'])
        organization = Organization(id=uuid.uuid4(), name=service_data['organization']['name'],
                                    url=service_data['organization']['url'])
        service = ORM_Service(id=uuid.uuid4(), name=service_data['name'], description=service_data['description'],
                              contact_url=service_data['contactUrl'],
                              documentation_url=service_data['documentationUrl'],
                              created_at=service_data['createdAt'], updated_at=service_data['updatedAt'],
                              environment=service_data['environment'], version=service_data['version'])
        service.type = service_type
        service.organization = organization
        url_orm.service = service

        try:
            db_session.add(service)
            db_session.commit()
        except orm.ORMException as e:
            print("Error writing to database: " + str(e), file=sys.stderr, flush=True)
            db_session.rollback()

    if "cohorts" not in service_data:
        cohort_url = urljoin(f"{url}/", "cohorts")
        cr = requests.get(cohort_url, timeout=1)
        if cr.status_code != 200:
            print(f"[{SERVICE_NAME}] No cohort data available at f{url}", file=sys.stderr, flush=True)
        else:
            service_data.update["cohorts"] = cr.json()

    return Service(**service_data), active


def get_service_data_from_db(service_orm):
    """
    Fetch service data from service_orm
    """
    if not service_orm:
        return None

    type_orm = service_orm.type
    organization_orm = service_orm.organization

    type_dict = orm.dump(type_orm, nonulls=False)
    type_dict.pop('id', None)

    org_dict = orm.dump(organization_orm, nonulls=False)
    org_dict.pop('id', None)

    service_dict = orm.dump(service_orm, nonulls=False)
    service_dict.pop('type_id', None)
    service_dict.pop('organization_id', None)
    service_dict['id'] = str(service_dict['id'])
    service_dict['type'] = type_dict
    service_dict['organization'] = org_dict

    pothole_to_camel_case = {'contact_url': 'contactUrl', 'documentation_url': 'documentationUrl',
                             'created_at': 'createdAt', 'updated_at': 'updatedAt'}

    for key in pothole_to_camel_case:
        service_dict[pothole_to_camel_case[key]] = service_dict.pop(key)

    return service_dict


@apilog
def list_services():
    """
    Return all known and active services
    """
    db_session = orm.get_session()
    try:
        urls = URL().query.all()
    except orm.ORMException as e:
        return Error(status=500, title='Error connecting to database', detail=str(e)), 500

    external_services = []
    for url in urls:
        service, active = get_service_info_and_active_status(url.url)
        if not service:
            continue
        # overwrite ID and name with local values
        service.id = url.id
        service.name = url.name
        service_as_dict = orm.dump(service)
        service_as_dict['url'] = url.url

        if options.show_active_status:
            service_as_dict['active'] = active

        external_services.append(ExternalService(**service_as_dict))

    return [orm.dump(ext_svc) for ext_svc in external_services], 200, {'Access-Control-Allow-Origin':'*'}


@apilog
def get_one_service(serviceId):
    """
    Return info for one service
    """
    db_session = orm.get_session()
    try:
        q = db_session.query(models.URL).get(serviceId)
    except orm.ORMException as e:
        return Error(status=500, title='Error connecting to database', detail=str(e)), 500

    if not q:
        return Error(title="No such service found", detail="No result for service "+str(serviceId), status=404), 404

    service, active = get_service_info_and_active_status(q.url)

    if not service:
        return Error(title="Service not available", detail="Could not connect to service "+str(serviceId), status=404), 404

    # overwrite ID and name with local values
    service.id = q.id
    service.name = q.name
    service_as_dict = orm.dump(service)
    service_as_dict['url'] = q.url

    if options.show_active_status:
        service_as_dict['active'] = active

    external_service = ExternalService(**service_as_dict)
    return orm.dump(external_service), 200, {'Access-Control-Allow-Origin':'*'}


@apilog
def get_this_service():
    """
    Return info for this service
    """
    return orm.dump(THIS_SERVICE), 200, {'Access-Control-Allow-Origin':'*'}


@apilog
def list_service_types():
    """
    Return all known and active services
    """
    db_session = orm.get_session()
    try:
        urls = URL().query.all()
    except orm.ORMException as e:
        return Error(status=500, title='Error connecting to database', detail=str(e)), 500

    service_types = []
    for url in urls:
        service, _ = get_service_info_and_active_status(url.url)
        if not service:
            continue
        service_type = ServiceType(**service.type)
        if not service_type in service_types:
            service_types.append(service_type)

    return [orm.dump(svc_type) for svc_type in service_types], 200, {'Access-Control-Allow-Origin':'*'}
