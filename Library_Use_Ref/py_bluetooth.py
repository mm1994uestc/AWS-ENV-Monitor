import bluetooth

print 'performing inquiry...'
nearby_devices = bluetooth.discover_devices(lookup_names = True)
print 'Found %d devices' % len(nearby_devices)
for addr,name in nearby_devices:
    print addr,'-',name
