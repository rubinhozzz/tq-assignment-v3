CREATE TABLE "orders" (
  "id" SERIAL PRIMARY KEY,
  "customer_id" int
);

CREATE TABLE "customers" (
  "id" int PRIMARY KEY,
  "name" varchar,
  "address" varchar
);

CREATE TABLE "barcodes" (
  "id" int PRIMARY KEY,
  "order_id" int
);

ALTER TABLE "orders" ADD FOREIGN KEY ("customer_id") REFERENCES "customers" ("id");

ALTER TABLE "barcodes" ADD FOREIGN KEY ("order_id") REFERENCES "orders" ("id");
