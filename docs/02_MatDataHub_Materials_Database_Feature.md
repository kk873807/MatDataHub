# MatDataHub Feature Deep Dive: Materials Database

## 1. Introduction
The **Materials Database** is the core foundational feature of MatDataHub. It allows engineers to search, filter, and discover material properties instantly, replacing the need to dig through massive PDF spec sheets or physical reference books.

## 2. Architecture & Logic

### Database Layer (`app/models.py`)
All materials are stored in a PostgreSQL table via Supabase. The SQLAlchemy ORM (Object-Relational Mapping) defines the material model:
- **Identifier:** `id`, `name`, `category` (e.g., Metal, Polymer).
- **Physical Properties:** `density` ($g/cm^3$).
- **Mechanical Properties:** `tensile_strength_min/max` ($MPa$), `yield_strength_min/max` ($MPa$), `elastic_modulus` ($GPa$), `hardness` ($HB$).
- **Thermal Properties:** `melting_point` ($°C$), `thermal_conductivity` ($W/m \cdot K$), `specific_heat` ($J/kg \cdot K$).
- **Economics:** `cost_per_kg_min/max` (₹/kg), `embodied_carbon` ($kg CO_2 / kg$).

### Backend Logic (`app/routers/materials.py`)
The backend provides a `GET /materials` endpoint.
- **Search Logic:** Uses SQL `ILIKE` pattern matching to instantly find materials matching a string (e.g., "Steel" or "Inconel").
- **Filtering Logic:** Allows passing specific category arrays to return only subset matches.
- **Pagination:** Uses `skip` and `limit` to ensure that even with millions of materials, the database does not crash the server. Only 20-50 materials are loaded per page.

### Frontend Component (`next-frontend/src/app/materials/page.tsx`)
- The frontend fetches the data from the backend and renders it in a beautiful, responsive Tailwind CSS grid.
- It includes a real-time search bar that debounces (waits for the user to stop typing for 300ms) before querying the backend to save API calls.
- **Material Detail View (`[id]/page.tsx`):** Clicking a material queries `GET /materials/{id}` and displays an exhaustive specification sheet.

## 3. The Mathematics of Material Indexing
To provide accurate sorting, the backend occasionally uses **fuzzy string matching** (via the `thefuzz` library) to handle typos in user searches (e.g., "Alluminum" instead of "Aluminum").

When determining average property values for display, the logic calculates the arithmetic mean of the ranges:
$$Average\_Strength = \frac{Tensile\_Min + Tensile\_Max}{2}$$

This ensures that engineers can compare materials based on a single unified metric even if the material has a wide tolerance range.
