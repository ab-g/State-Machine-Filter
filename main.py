import sys
import os
import json


def get_first_state_machine_id(resource_pack_data):
    return resource_pack_data['stateMachines']['map'][0]['value']['id']['uuid']


def main(game_project_dir_path, states_names):
    resource_pack_file_path = os.path.join(game_project_dir_path, 'resource-pack.json')
    with open(resource_pack_file_path, 'r') as resource_pack_file:
        resource_pack_data = json.load(resource_pack_file)

    state_machine_id = get_first_state_machine_id(resource_pack_data)
    state_machine_file_path = os.path.join(game_project_dir_path, 'state-machines/{0}.json'.format(state_machine_id))

    with open(state_machine_file_path, 'r') as state_machine_file:
        state_machine_data = json.load(state_machine_file)

        state_machine_data['states'] = [
            state for state in state_machine_data['states']
            if any(state['displayName'] in state_name for state_name in states_names)
        ]

        state_machine_data['behavior']['transitions'] = [
            transition for transition in state_machine_data['behavior']['transitions']
            if any(transition['source_id'] == state['id'] for state in state_machine_data['states'])
                and any(transition['dest_id'] == state['id'] for state in state_machine_data['states'])
        ]

        print(json.dumps(state_machine_data, indent=4))

    with open(state_machine_file_path, 'w') as state_machine_file:
        json.dump(state_machine_data, state_machine_file, indent=4, sort_keys=False)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2].split(','))
