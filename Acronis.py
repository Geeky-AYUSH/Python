import requests
import json
import pprint
client_id = 'e2c0a770-5dca-4886-8ca5-00d5ab90f97d'
client_secret = 'e5z3ptddrqifcryy23ky7cymsy3fdh6tthkddvojkdxdav2lqnym'
datacenter_url = 'https://sg-cloud.acronis.com'

base_url = f'{datacenter_url}/api/2'
base_url
from base64 import b64encode
encoded_client_creds = b64encode(f'{client_id}:{client_secret}'.encode('ascii'))
basic_auth = {
     'Authorization': 'Basic ' + encoded_client_creds.decode('ascii')
}
response = requests.post(
     f'{base_url}/idp/token',
     headers={'Content-Type': 'application/x-www-form-urlencoded', **basic_auth},
     data={'grant_type': 'client_credentials'},
 )

token_info = response.json()
pprint.pprint(token_info)
auth = {'Authorization': 'Bearer ' + token_info['access_token']}
auth
base_url = f'{datacenter_url}/api'
base_url
from uuid import uuid4
protection_plan_id = str(uuid4())
protection_plan_id
Plan_name = input("provide your plan_name")
plan_data = {
     'subject': {
         'policy': [
             {
                 'id': protection_plan_id,
                 'type': 'policy.protection.total',
                 'origin': 'upstream',
                 'enabled': True,
                 'name': Plan_name
             }
         ]
     }
 }
policies = [
    {
        "id": str(uuid4()),
        # Machine backup policy type is 'policy.backup.machine'
        'type': 'policy.backup.machine',
        'parent_ids': [
            protection_plan_id
        ],
        'origin': 'upstream',
        'enabled': True,
        'settings_schema': '2.0',
        'settings': {
            # Archive compression level. Available values: ``normal``, ``high``, ``max``. When value is not specified - no compression is applied.
            'compression': 'normal',
            # Format of the Acronis backup archive. Available values: ``11``, ``12``, ``auto``.
            'format': 'auto',
            # If true, snapshots of multiple volumes will be taken simultaneously. Equals to false if value is not specified.
            'multi_volume_snapshotting_enabled': True,
            # If true, the file security settings will be preserved. Equals to false if value is not specified.
            'preserve_file_security_settings': True,
            # Configuration of retries on recoverable errors during the backup operations like reconnection to destination. No attempts to fix recoverable errors will be made if retry configuration is not set.
            'reattempts': {
                # If true, enables retry on recoverable errors.
                'enabled': True,
                # An interval between retry attempts.
                'interval': {
                    # A type of the interval. Available values are: ``seconds``, ``minutes``, ``hours``, ``days``.
                    'type': 'seconds',
                    # The amount of value specified in ``interval.type``.
                    'count': 30
                },
                # Max number of retry attempts. Operation will be considered as failed when max number of retry attempts is reached.
                'max_attempts': 30
            },
            # If true, a user interaction will be avoided when possible. Equals to false if value is not specified.
            'silent_mode_enabled': True,
            # Determines the size to split backups on. Splitting is not performed if value is not specified.
            'splitting': {
                # The size of split backup file in bytes.
                'size': 9223372036854775807
            },
            # Configuration of retries on errors during the creation of the virtual machine snapshot. No attempts to fix recoverable errors will be made if retry configuration is not set.
            'vm_snapshot_reattempts': {
                # If true, enables retry on errors.
                'enabled': True,
                # Configuration of the interval between retry attempts.
                'interval': {
                    # A type of the interval. Available values are: ``seconds``, ``minutes``, ``hours``, ``days``.
                    'type': 'minutes',
                    # The amount of value specified in ``interval.type``.
                    'count': 5
                },
                # Max number of retry attempts. Operation will be considered as failed when max number of retry attempts is reached.
                'max_attempts': 3
            },
            # Settings for the Volume Shadow Copy Service (VSS) provider. If not set, no VSS provider is used.
            'vss': {
                # If true, the VSS will be enabled.
                'enabled': True,
                # A type of VSS provider to use in backup. Only ``native`` and ``target_system_defined`` options are available.
                'provider': 'target_system_defined'
            },
            # The archive properties.
            'archive': {
                # The name of the generated archive. The name may use the following variables: ``[Machine Name]``, ``[Plan ID]``, ``[Plan Name]``, ``[Unique ID]``, ``[Virtualization Server Type]``.
                'name': '[Machine Name]-[Plan ID]-[Unique ID]A'
            },
            # Time windows for performance limitations of backup and storage maintenance operations.
            "performance_window": {
                "enabled": True,
                # A tuple of 3 presets
                "presets": [
                    {
                        # CPU priority - 'idle', 'low', 'normal', 'high', 'realtime'
                        "cpu_priority": "normal",
                        "disk_limit": {
                            # Value in specified units
                            "value": 50,
                            # Units. 'percent' - percentage, 'speed' - speed in kilobytes
                            "type": "percent"
                        },
                        # ID of preset. 'high' - green, 'low' - blue, 'cancel' - gray.
                        "id": "high",
                        "network_limit": {
                            # Value in specified units
                            "value": 50,
                            # Units. 'percent' - percentage, 'speed' - speed in kilobytes per second
                            "type": "percent"
                        },
                        # List of timetable objects
                        "timetable": [
                            {
                                # Time from which the preset applies
                                "time_from": {
                                    "hour": 0,
                                    "minute": 0
                                },
                                # Time until the preset applies
                                "time_to": {
                                    "hour": 23,
                                    "minute": 59,
                                    "second": 59
                                },
                                # Days of week in three-letter format
                                "days_of_week": [
                                    "sun",
                                    "mon",
                                    "tue",
                                    "wed",
                                    "thu",
                                    "fri",
                                    "sat"
                                ]
                            }
                        ]
                    },
                    {
                        "cpu_priority": "high",
                        "disk_limit": {
                            "value": 25,
                            "type": "percent"
                        },
                        "id": "low", # Blue preset
                        "network_limit": {
                            "value": 25,
                            "type": "percent"
                        },
                        "timetable": [
                            {
                                "time_from": {
                                    "hour": 8,
                                    "minute": 0
                                },
                                "time_to": {
                                    "hour": 8,
                                    "minute": 59,
                                    "second": 59
                                },
                                "days_of_week": [
                                    "sun",
                                    "fri"
                                ]
                            }
                        ]
                    },
                    {
                        "id": "cancel", # Gray (inactive) preset
                        "network_limit": {
                            "value": 100,
                            "type": "percent"
                        },
                        "disk_limit": {
                            "value": 100,
                            "type": "percent"
                        },
                        "timetable": [
                            {
                                "time_from": {
                                    "hour": 8,
                                    "minute": 0
                                },
                                "time_to": {
                                    "hour": 15,
                                    "minute": 59,
                                    "second": 59
                                },
                                "days_of_week": [
                                    "mon"
                                ]
                            }
                        ]
                    }
                ],
            },
            # Configuration of backup retention rules.
            'retention': {
                # A list of retention rules.
                'rules': [
                    {
                        # A list of backup sets where rules are effective.
                        'backup_set': [
                            'daily'],
                        # Configuration of the duration to keep backups in archive created by the policy.
                        'max_age': {
                            # A type of the duration. Available values are: ``seconds``, ``minutes``, ``hours``, ``days``.
                            'type': 'days',
                            # The amount of value specified in ``max_age.type``.
                            'count': 7
                        }
                    }
                ],
                # If true, retention rules will be applied after backup is finished.
                'after_backup': True
            },
            # Storage location of the archives.
            'vault': {
                # Type of storage location. Available values: ``local_folder``, ``network_share``, ``ftp``, ``sftp``, ``cd``, ``tape``, ``storage_node``, ``asz``, ``removable``, ``cloud``, ``nfs_share``, ``esx``, ``astorage2``, ``script``.
                'type': 'cloud',
                # If true, the vault will be accessed using the policy credentials.
                'use_policy_credentials': True
            },
            # Configuration of policy-related alerts.
            'alerts': {
                # If true, the alerts will be enabled.
                'enabled': False,
                # Number of days that will trigger the alert about the passed number of days without a backup.
                'max_days_without_backup': 5
            },
            # Configuration of the backup schedule.
            'scheduling': {
                # A list of schedules with backup sets that compose the whole scheme.
                'backup_sets': [
                    {
                        'type': 'auto',
                        'schedule': {
                            'alarms': {
                                'time': {
                                    'weekdays': [
                                        'mon',
                                        'tue',
                                        'wed',
                                        'thu',
                                        'fri'
                                    ],
                                    'repeat_at': [
                                        {
                                            'hour': 21,
                                            'minute': 0
                                        }
                                    ]
                                }
                            },
                            'conditions': {},
                            'prevent_sleep': True,
                            'type': 'weekly'
                        }
                    }
                ],
                # If true, the backup schedule will be enabled.
                'enabled': True,
                # Max number of backup processes allowed to run in parallel. Unlimited if not set.
                'max_parallel_backups': 2,
                'rand_max_delay': {  # Configuration of the random delay between the execution of parallel tasks.
                    # A type of the duration. Available values are: ``seconds``, ``minutes``, ``hours``, ``days``.
                    'type': 'minutes',
                    # The amount of value specified in ``rand_max_delay.type``.
                    'count': 30
                },
                # A backup scheme. Available values: ``simple``, ``always_full``, ``always_incremental``, ``weekly_incremental``, ``weekly_full_daily_incremental``, ``custom``, ``cdp``.
                'scheme': 'always_incremental',
                "task_failure": {
                    "enabled": True,
                    "interval": {
                        "type": "hours", # Time units - hours, minutes, seconds
                        "count": 1 # Number of time units
                    },
                    "max_attempts": 12 # Number of attempts between task restarts
                },
                # A day of week to start weekly backups in 3-letter abbreviation format.
                'weekly_backup_day': 'mon'
            },
            # A configuration of Changed Block Tracking (CBT). Available values: ``use_if_enabled``, ``enable_and_use``, ``do_not_use``.
            'cbt': 'enable_and_use',
            # If true, determines whether a file has changed by the file size and timestamp. Otherwise, the entire file contents are compared to those stored in the backup.
            'fast_backup_enabled': True,
            # If true, a quiesced snapshot of the virtual machine will be taken.
            'quiesce_snapshotting_enabled': True
        }
    },
    # Put other policy objects here.
]
plan_data['subject']['policy'] += policies
plan_data = json.dumps(plan_data, indent=4)
response = requests.post(
     f'{base_url}/policy_management/v4/policies',
     headers={'Content-Type': 'application/json', **auth},
     data=plan_data,
)
response.status_code
response2 = requests.get(f'{base_url}/resource_management/v4/resources', headers=auth)
response2.status_code
resources = response2.json()['items']
desired_id = None
hostname = input("hostname_of_server")
for item in resources:
    if item['name'] == hostname:
        desired_id = item['id']
        break

print(desired_id)
application_data = {
    'policy_id': protection_plan_id,
    'context': {
        'items': [
            desired_id
        ]
    }
}
application_data = json.dumps(application_data, indent=4)
response = requests.post(
     f'{base_url}/policy_management/v4/applications',
     headers={'Content-Type': 'application/json', **auth},
     data=application_data,
 )
response.status_code
