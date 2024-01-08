from commands.delete import Delete
from commands.get import Get
from commands.info import Info
from commands.keys import Keys
from commands.set import Set


async def processor(command, credentials, data):
    value = None
    if command == 'set':
        value = await Set.execute(credentials, data)
    elif command == 'get':
        value = await Get.execute(credentials, data)
    elif command == 'delete':
        value = await Delete.execute(credentials, data)
    elif command == 'keys':
        value = await Keys.execute(credentials, data)
    elif command == 'info':
        value = await Info.execute(credentials, data)

    return value