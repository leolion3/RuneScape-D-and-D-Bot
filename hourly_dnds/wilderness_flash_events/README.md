# Wilderness Flash Events Module

This module notifies you about the next upcoming event within the hour.

If you dont wish to receive notifications for all events, you can enable the
`` in the application's `.env` file by setting the value to `true`.

## Setting Favourites

The provided `config.json` file contains the key `favourite_events`. Here you
can add any events you want, separated by commas. A valid config looks like this:

```json
{
  "favourite_events": [
    "Spider Swarm",
    "Unnatural Outcrop",
    "Stryke the Wyrm",
    "Demon Stragglers",
    "Butterfly Swarm",
    "King Black Dragon Rampage",
    "Forgotten Soldiers",
    "Surprising Seedlings",
    "Hellhound Pack",
    "Infernal Star",
    "Lost Souls",
    "Ramokee Incursion",
    "Displaced Energy",
    "Evil Bloodwood Tree"
  ]
}
```

(\*) Note the **BRITISH** spelling of `favourites`.

To enable or disable any of the events, simply remove them from the list and
restart the application.

> **The default list of favourite events are those that grant very wildy rewards.**
