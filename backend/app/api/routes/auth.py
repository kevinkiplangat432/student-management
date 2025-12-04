from fastapi import APIRouter # api router from Fastapi

# create a router instance which will hold allauth related endpoints
router = APIRouter() 

#get the end point.
@router.get()
def auth_status():
    return {}




#study:
# apirouter allows me to group related endpoints together.