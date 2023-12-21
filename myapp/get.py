

# def getcam():
#     cam = 'qwe'
#     return cam


# def getinfo(id):
#     employee == id
#     print(employee)
#     return employee

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JeztX.settings')
django.setup()

from myapp.models import EmployeeCameraAssignment

def list_all_cameras():
    # Fetch all unique cameras from EmployeeCameraAssignment
    camera_assignments = EmployeeCameraAssignment.objects.select_related('camera').distinct('camera')
    cameras = [assignment.camera for assignment in camera_assignments]
    print(cameras)
    return cameras

list_all_cameras()


