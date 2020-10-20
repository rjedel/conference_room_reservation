# Conference Room Reservation

It is a simple web application for booking conference rooms in office building. The application was created using the Django framework. The user can only book rooms for the whole day.

## Main page:

Upon entering the home page, the user sees all conference rooms and their status as of today. Next to the name of each room, there are buttons for modifying the room data, deleting it, and booking a room

## Detailed view of the conference room:

After clicking on the room name, the user will see all the room data:

1.  name of the room,
2.  capacity,
3.  whether it has an overhead projector.

Additionally, a list of days on which the room will be unavailable is displayed. User can not see days from the past. There are buttons that:

1.  will allow to book this room,
2.  delete this room,
3.  modify this room.

## Adding a new room

The user can add a new room.

## Editing the room

After entering the room edition page, the user may enter the room data (name, capacity, projector).

## Reservation of the room

After entering the room booking website, the user will again see the list of days when the room will be occupied (no days from the past are visible). User can enter the date of booking a given room. The system makes sure not to duplicate the reservation on a given day for a given room and that the date is not from the past.

## Searching for a room

The user can search for rooms with the following conditions:

1.  name of the room,
2.  room capacity,
3.  projector availability.