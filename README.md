# Guidance for Task

This project is focused on implementing user profile management with avatar upload capabilities in a FastAPI application. You are expected to work with a single in-memory user profile that can be viewed, updated, and associated with an uploaded avatar image.

The core requirements are:
- Provide endpoints to view and update the user profile (username, display name, and bio) with input validation.
- Enable uploading an avatar image file, strictly limiting types to JPEG and PNG, and files to a maximum size.
- All uploads must be stored in a secure local directory, and avatars must be available for download via a static URL endpoint.
- Appropriately respond to error conditions such as invalid data, unsupported file types, or files that are too large.

No user authentication or persistent storage is needed—work with the provided single in-memory profile.

## Verifying Your Solution

You can verify your implementation by interacting with the API endpoints:
- View the profile via `GET /profile`.
- Update the profile data using `PUT /profile` with validated values.
- Upload an avatar using `POST /profile/avatar` (constraints apply).
- Retrieve the uploaded avatar from its `/avatars/{filename}` URL after a successful upload.

Error codes and validation messaging must be handled in accordance with the specification. Interact with these endpoints from a test client or API tool to confirm expected behavior. Make sure the code is production-like, robust, and meets all outlined requirements.