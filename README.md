# MessageDeliverySystem
This project designs and implements a message delivery system using Python. It includes the following parts:

HUB:

The Hub relays incoming message bodies to receivers based on user ID(s) defined in the message. The hub can for example assign arbitrary (unique) user id to the clients as they connect.

 - user_id - unsigned 64 bit integer
 - Connection to hub is done using pure TCP.

CLIENTS:

Clients are users who are connected to the hub. Client can send three types of messages which are described below.

Identity message - 

A Client can send an identity message which the hub will respond with the user_id of the connected user.

List message - 

Client can send a command to list messages, which cause the hub to answer with the list of all connected client user_ids (excluding the requesting client).

Relay message -

Clients can send relay messages where the body of the message is relayed to the receivers marked in the message. The message body can be relayed to one or multiple receivers.

 - max 255 receivers (user_id:s) per message
 - message body - byte array (text, JSON, binary, or anything), max length 1024 kilobytes
