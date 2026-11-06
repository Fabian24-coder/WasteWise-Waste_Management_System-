# WasteWise-Waste_Management_System-
This is a web application built with Python and Django designed to make garbage collection simple, organized, and efficient for residents and waste collection teams.
# What We Are Trying to Achieve
This project aims to:
#
**-Connect Residents and Collectors:** Give everyday users an easy way to request pickups while helping collectors manage their daily routes and assigned areas.
#
**-Track Waste Clearly:** Standardize waste categories, weights, and pricing so everyone knows what is being collected and how much it costs.
#
**Keep Payments Transparent:** Keep tabs on payment statuses and amounts linked directly to specific collection requests. 

# How the System Works (Key Features)
#
**-User Accounts & Profiles:** Users can sign up, log in, and save their specific addresses, phone numbers, and location details so collectors can easily find them.
#
**-Rubbish Details:** Defines the types of waste accepted, including categories, pricing rates, weights, and descriptions.
#
**-Pickup Requests:** Requestors create requests for specific types of waste. Collectors accept and schedule or decline requests, and requestors confirm payment and collection. The system tracks each request's status.
#
**-Collector Details:** Manages collector profiles, including their names, contact details, and assigned working zones.
#
**-Payments:** Tracks financial transactions for each pickup, logging the amount, payment date, and status.
#
# Request and collection workflow

- The server-rendered Django pages use the WasteWise styles from [WastewiseSystemTeam/WasteWise-Waste_Management_System-#6](https://github.com/WastewiseSystemTeam/WasteWise-Waste_Management_System-/pull/6). Dashboard, request, sign-in, registration, and admin rate pages use the Django database and session authentication; the prototype's LocalStorage demo behavior is not used.
- Requestors can register at `/accounts/register/`, sign in at `/accounts/login/`, and submit collection requests from the pickup dashboard. Each request records contact details, address, requested collection date, waste type, quantity, and estimated distance in kilometres.
- Admins maintain the waste rate table in Django Admin or the Waste Types page. Each waste type has a price per unit and an additional distance charge per kilometre. The quoted fee is `(quantity × unit rate) + (distance in km × distance rate per km)`. Rates and the calculated fee are saved with the request so later rate changes do not alter existing quotes. Configure rates in the project's chosen currency; no currency is assumed by the application.
- A new request starts with status `new` and payment method `cash`. Collectors can accept it with a scheduled date/time and message, or decline it with a reason. Requestors see that update on their dashboard.
- On the scheduled collection day, the requestor confirms cash payment and then confirms collection. The status changes to `collected`, which is visible to collectors.
- Roles are `requestor`, `collector`, and `admin`. Public registration always creates a requestor account; admins create or promote collector accounts from Django Admin.

# API workflow

Pickup API routes are under `/pickups/api/v1/` and require authentication. Register and obtain a token using `/api/auth/register/` and `/api/auth/login/`; send the token as `Authorization: Token <token>`. Swagger UI also supports the token through its **Authorize** button. Public registration creates requestor accounts only.

- `GET waste-rates/` lists active waste types and rates.
- `POST create/` creates a request. Supply `contact_name`, `contact_number`, `address`, `collection_date` (`YYYY-MM-DD`), `waste_type` (rate-table ID), `quantity`, and `distance_km`.
- `GET list/` returns all requests for collectors/admins and only the signed-in requestor's requests otherwise.
- `POST <id>/decision/` lets a collector accept (`action: "accept"` plus `scheduled_collection_at`) or decline (`action: "decline"` plus `decline_reason`). An optional `collector_message` is shown to the requestor.
- `POST <id>/payment/` confirms cash payment for the requestor's own accepted request on the scheduled day.
- `POST <id>/confirm-collection/` confirms collection after payment on the scheduled day.
- `PUT`/`PATCH update/<id>/` and `DELETE delete/<id>/` are admin-only.
- Authenticated users can read `/api/zones/` and `/api/collectors/`; zone and collector profile changes are admin-only. A collector profile must reference a user with the collector role.
- The interactive API schema is available at `/api/docs/`.
#
# Attached is the Entity Relation Diagram(ERD)
Suggestions and improvement are welcome
<img width="440" height="544" alt="image" src="https://github.com/user-attachments/assets/90aa9bf7-86bb-4ad5-aaa0-7357d0e3657e" />
