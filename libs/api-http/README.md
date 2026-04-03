# api-http

Reusable internal Django library for class-based, decorator-driven HTTP controllers.

## Exports

- `@controller(prefix=...)`
- `@get/@post/@put/@patch/@delete` and `@route`
- `@use(...)` (class/method hook bridge for decorators like `login_required`)
- `Controller` base class with JSON response helpers
- `build_urlpatterns(...)` URL adapter
- `ApiHttpError` family and uniform JSON error mapping
