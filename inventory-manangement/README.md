# Inventory Management

## Characteristics and Functionalities

- `Resource` base class provides common attributes and functionalities to all electronic resources (CPU, HDD, SSD):
  - `name`: resource name, e.g., Intel Core i9-9900K
  - `manufacturer`: resource manufacturer, e.g., Nvidia
  - `total`: current total count of resource
  - `allocated`: current count of in-use resource
  - `category`: resource category, computed property
  - `available`: current count of available resource, computed property
  - `__str__`: representation returning resource name
  - `__repr__`: detailed representation
  - `allocate(count)` : method to allocate count of resource items if available
  - `freeup(count)` : method to reset count of allocated resource items, if not more than allocated, to be available
  - `died(count)` : method to remove count of allocated resource items, if not more than allocated, from total and allocated
  - `purchased(count)` - method to add count of new resource items to total
- `CPU` subclass provides extra CPU-specific attributes to all CPUs:
  - `cores`: number of cores
  - `socket`: socket type
  - `power_watts`: rated wattage
  - `__repr__`: extended detailed representation
- `Storage` subclass provides extra storage-specific attributes to all storage devices:
  - `capacity_gb`: storage capacity in GB
  - `__repr__`: extended detailed representation
- `HDD` subclass provides extra HDD-specific attributes to all HDD storage devices:
  - `size`: device size, 2.5" or 3.5"
  - `rpm`: disk rotation speed in rpm
  - `__repr__`: extended detailed representation
- `SSD` subclass provides extra SSD-specific attributes to all SSD storage devices:
  - `interface`: device interface, e.g. PCIe NVMe 3.0 x4
  - `__repr__`: extended detailed representation

## Tests

Unit tests are implemented with `pytest` for all classess and methods.
