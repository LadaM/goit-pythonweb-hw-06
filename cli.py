import argparse
import logging
from sqlalchemy.exc import IntegrityError
from connect import session
from models import Teacher, Group, Student, Subject, Grade

logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

MODEL_MAP = {
    "teacher": Teacher,
    "Teacher": Teacher,
    "student": Student,
    "Student": Student,
    "group": Group,
    "Group": Group,
    "subject": Subject,
    "Subject": Subject,
    "grade": Grade,
    "Grade": Grade,
}

def log_error(message):
    logging.error(message)
    print(message)

def safe_add(entity):
    while True:
        try:
            session.add(entity)
            session.commit()
            print(f"{entity.__class__.__name__} '{entity}' created.")
            break
        except IntegrityError:
            session.rollback()
            log_error(f"ID conflict for {entity}. Incrementing ID and retrying.")
            if hasattr(entity, "id"):
                entity.id += 1

def create_entity(model, **kwargs):
    if model == Student and "group_id" in kwargs:
        group = session.query(Group).filter_by(id=kwargs["group_id"]).first()
        if not group:
            log_error(f"Group with ID {kwargs['group_id']} does not exist.")
            return
    entity = model(**kwargs)
    safe_add(entity)

def list_entities(model):
    entities = session.query(model).all()
    for entity in entities:
        print(entity)

def update_entity(model, entity_id, **kwargs):
    entity = session.query(model).filter_by(id=entity_id).first()
    if entity:
        for key, value in kwargs.items():
            setattr(entity, key, value)
        session.commit()
        print(f"{model.__name__} with ID {entity_id} updated.")
    else:
        log_error(f"{model.__name__} with ID {entity_id} not found.")

def delete_entity(model, entity_id):
    entity = session.query(model).filter_by(id=entity_id).first()
    if entity:
        session.delete(entity)
        session.commit()
        print(f"{model.__name__} with ID {entity_id} deleted.")
    else:
        log_error(f"{model.__name__} with ID {entity_id} not found.")

def main():
    parser = argparse.ArgumentParser(description="CLI for CRUD operations on the database.")
    parser.add_argument("-a", "--action", required=True, choices=["create", "list", "update", "remove"], help="Action to perform.")
    parser.add_argument("-m", "--model", required=True, choices=MODEL_MAP.keys(), help="Model to perform the action on.")
    parser.add_argument("-i", "--id", type=int, help="ID of the record to update or delete.")
    parser.add_argument("-n", "--name", help="Name for creation or update.")
    parser.add_argument("--group-id", type=int, help="Group ID for students.")
    parser.add_argument("--teacher-id", type=int, help="Teacher ID for subjects.")

    args = parser.parse_args()

    model = MODEL_MAP[args.model]

    if args.action == "create":
        if model == Student:
            if args.name and args.group_id:
                create_entity(model, name=args.name, group_id=args.group_id)
            else:
                print("Name and group_id are required for creating a student.")
        elif model == Subject:
            if args.name and args.teacher_id:
                create_entity(model, name=args.name, teacher_id=args.teacher_id)
            else:
                print("Name and teacher_id are required for creating a subject.")
        elif args.name:
            create_entity(model, name=args.name)
        else:
            print("Name is required for creating this entity.")

    elif args.action == "list":
        list_entities(model)

    elif args.action == "update":
        if args.id:
            update_data = {}
            if args.name:
                update_data["name"] = args.name
            if model == Student and args.group_id:
                update_data["group_id"] = args.group_id
            if update_data:
                update_entity(model, args.id, **update_data)
            else:
                print("No data provided for update.")
        else:
            print("ID is required for update.")

    elif args.action == "remove":
        if args.id:
            delete_entity(model, args.id)
        else:
            print("ID is required for remove.")

if __name__ == "__main__":
    main()