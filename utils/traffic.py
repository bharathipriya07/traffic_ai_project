def get_signal_time(vehicle_count):
    if vehicle_count < 10:
        return 15
    elif vehicle_count < 30:
        return 30
    else:
        return 60