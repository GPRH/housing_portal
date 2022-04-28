from django.core.management import call_command

# add the layer to be mapped here...
mappings = {
    'building_confidence':
    'colombia/cartagena/el_pozon/buildings/building_confidence_values.csv',
}


def get_path(file):
    shape_dir = '/imports/'
    return '{0}{1}'.format(shape_dir, file)


def generate_models(model_name, shape_file):
    shape_path = get_path(shape_file)
    model_path = get_path('{0}.py'.format(model_name))
    with open(model_path, 'w') as f:
        call_command('ogrinspect', shape_path,
                     model_name, '--mapping', stdout=f)


def run():
    print('Generating model mappings')
    for model_name, shape_file in mappings.items():
        generate_models(model_name, shape_file)
