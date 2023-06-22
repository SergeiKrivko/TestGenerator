def bash_run(path, sm, cm, args='', in_data='', coverage=False, scip_timeout=False):
    if scip_timeout:
        return cm.cmd_command(f"\"{path}\" {args}", input=in_data, shell=True)
    return cm.cmd_command(f"\"{path}\" {args}", input=in_data, shell=True, timeout=float(sm.get_smart('time_limit', 3)))


def batch_run(path, sm, cm, args='', in_data='', coverage=False, scip_timeout=False):
    if scip_timeout:
        return cm.cmd_command(f"\"{path}\" {args}", input=in_data, shell=True)
    return cm.cmd_command(f"\"{path}\" {args}", input=in_data, shell=True, timeout=float(sm.get_smart('time_limit', 3)))
