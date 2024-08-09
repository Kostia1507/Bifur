from datetime import datetime, timedelta

cooldownTime = []
cooldownUser = []

default_cooldown = 1


def setCooldown(user_id):
    if user_id in cooldownUser:
        for i in range(len(cooldownUser)):
            if cooldownUser[i] == user_id:
                cooldownTime[i] = datetime.now()
                break
    else:
        cooldownUser.append(user_id)
        cooldownTime.append(datetime.now())


def setSpecialCooldown(user_id, time=30):
    if user_id in cooldownUser:
        for i in range(len(cooldownUser)):
            if cooldownUser[i] == user_id:
                cooldownTime[i] = datetime.now() + timedelta(seconds=time)
                break
    else:
        cooldownUser.append(user_id)
        cooldownTime.append(datetime.now() + timedelta(seconds=time))


def isInCooldown(user_id):
    if user_id in cooldownUser:
        for i in range(len(cooldownUser)):
            if cooldownUser[i] == user_id:
                return datetime.now() < cooldownTime[i] + timedelta(seconds=default_cooldown)
    else:
        return False


def removeCooldown(user_id):
    if user_id in cooldownUser:
        for i in range(len(cooldownUser)):
            if cooldownUser[i] == user_id:
                cooldownTime[i] = datetime.now() - timedelta(seconds=60)


def toString():
    res = ''
    for i in range(len(cooldownUser)):
        res += str(cooldownUser[i]) + ' ' + str(cooldownTime[i]) + '\n'
    return res
