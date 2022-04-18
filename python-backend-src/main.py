import sys

if __name__ == '__main__':
    action = sys.argv[1]
    if action == 'process_data':
        # NB lazy import modules
        from tasks.process_data import process_data
        process_data()
    elif action == 'train_classifier':
        # NB lazy import modules
        from tasks.train_classifier import train_classifier
        train_classifier()
    elif action == 'flask_app':
        # NB lazy import modules
        from tasks.flask_app import flask_app
        flask_app()
    else:
        raise Exception(f"Unrecognised action {action}")
        exit(1)
