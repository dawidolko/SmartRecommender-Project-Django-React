### Relationships in the given database

---

#### 1. **`User`** Relationships

- **`user`** Table:

- Inherits from `AbstractUser`.

- Contains `role` field with choices `admin` and `client`.

---

#### 2. **`Product`** Relationships

- **`product`** Table:

- Has foreign key to `sale` (`SET NULL` on deletion).

- Many-to-many (`ManyToMany`) with `category` via intermediate table `product_category`.

---

#### 3. **`Category`** Relationships

- **`category`** Table:

- In many-to-many relationship with `product` via intermediate table `product_category`.

---

#### 4. **`Sale`** Relationships

- **`sale`** Table:
- In relation to `product` as a foreign key.

---

#### 5. **`ProductCategory`** Intermediate Table

- **`product_category`** Table:
- Foreign key to `product` and `category`.
- Unique relation between `product` and `category` (`unique_together`).

---

#### 6. **`PhotoProduct`** Relationships

- **`photo_product`** Table:
- Foreign key to `product` (`CASCADE` on deletion).

---

#### 7. **`Opinion`** Relationships

- **`opinion`** Table:
- Foreign key to `product` (`CASCADE` if deleted).
- Foreign key to `user` (`CASCADE` if deleted).

---

#### 8. **`Order`** Relationships

- **`order`** Table:
- Foreign key to `user` (`CASCADE` if deleted).

---

#### 9. **`OrderProduct`** Intermediate Table

- **`order_product`** Table:
- Foreign key to `order` (`CASCADE` if deleted).

---

#### 10. **`Complaint`** Relationships

- **`complaint`** Table:
- Foreign key to `order` (`CASCADE` if deleted).

---

#### 11. **`Specification`** Relationships

- **`specification`** Table:
- Foreign key to `product` (`CASCADE` if deleted).

---

### ERD Schema (descriptive)

1. **`user`**:

- `1:N` relation to `order`.
- `1:N` relation to `opinion`.

2. **`category`**:

- `N:M` relation to `product` via `product_category`.

3. **`product`**:

- `1:N` relation to `photo_product`.
- Relationship `1:N` with `opinion`.
- Relationship `N:M` with `order` via `order_product`.
- Relationship `1:N` with `specification`.

4. **`sale`**:

- Relationship `1:N` with `product`.

5. **`order`**:

- Relationship `1:N` with `order_product`.
- Relationship `1:N` with `complaint`.

---
