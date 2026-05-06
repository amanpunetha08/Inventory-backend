from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from inventory.db import db

notifications_collection = db['notifications']


def serialize_notification(n):
    n['id'] = str(n.pop('_id'))
    return n


def create_notification(user, message, ntype='info'):
    notifications_collection.insert_one({
        'user': user,
        'message': message,
        'type': ntype,
        'read': False,
        'created_at': datetime.utcnow(),
    })


@api_view(['GET'])
def notifications_list(request):
    notes = list(notifications_collection.find({'user': request.user.username}).sort('created_at', -1).limit(50))
    unread = notifications_collection.count_documents({'user': request.user.username, 'read': False})
    return Response({'notifications': [serialize_notification(n) for n in notes], 'unread_count': unread})


@api_view(['POST'])
def mark_read(request, notification_id):
    try:
        oid = ObjectId(notification_id)
    except Exception:
        return Response({'error': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)
    notifications_collection.update_one({'_id': oid, 'user': request.user.username}, {'$set': {'read': True}})
    return Response({'status': 'ok'})


@api_view(['POST'])
def mark_all_read(request):
    notifications_collection.update_many({'user': request.user.username, 'read': False}, {'$set': {'read': True}})
    return Response({'status': 'ok'})
