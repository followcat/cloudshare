class ExecTimeout(BaseException):
    pass


class KilledExecTimeout(ExecTimeout):
    pass


class FailedKillExecTimeout(ExecTimeout):
    pass


class NotKillExecTimeout(ExecTimeout):
    pass
