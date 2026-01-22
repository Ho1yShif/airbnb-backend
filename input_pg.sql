
-- PostgreSQL-compatible schema for Airbnb Clone (public schema, no duplicates)

CREATE TABLE IF NOT EXISTS attribute_category (
  attribute_category_id SERIAL PRIMARY KEY,
  category_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS attribute (
  attribute_id SERIAL PRIMARY KEY,
  attribute_category_id INT NOT NULL REFERENCES attribute_category(attribute_category_id) ON DELETE CASCADE,
  attribute_name VARCHAR(255) NOT NULL,
  description TEXT
);

CREATE TABLE IF NOT EXISTS region (
  region_id SERIAL PRIMARY KEY,
  region_name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS country (
  country_id SERIAL PRIMARY KEY,
  region_id INT NOT NULL REFERENCES region(region_id) ON DELETE CASCADE,
  country_name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS location (
  location_id BIGSERIAL PRIMARY KEY,
  country_id INT NOT NULL REFERENCES country(country_id) ON DELETE CASCADE,
  city VARCHAR(255) NOT NULL,
  address VARCHAR(255),
  location_name VARCHAR(255),
  latitude DECIMAL(10,8),
  longitude DECIMAL(11,8)
);

CREATE TABLE IF NOT EXISTS place_type (
  place_type_id SERIAL PRIMARY KEY,
  type_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS property_type (
  property_type_id SERIAL PRIMARY KEY,
  type_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS user_account (
  id BIGSERIAL PRIMARY KEY,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  email_address VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  phone VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- property
CREATE TABLE IF NOT EXISTS property (
  property_id BIGSERIAL PRIMARY KEY,
  location_id BIGINT NOT NULL REFERENCES location(location_id) ON DELETE CASCADE,
  place_type_id INT NOT NULL REFERENCES place_type(place_type_id),
  property_type_id INT NOT NULL REFERENCES property_type(property_type_id),
  host_id BIGINT NOT NULL REFERENCES user_account(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price_per_night DECIMAL(10,2) NOT NULL,
  number_guests INT NOT NULL,
  num_beds INT NOT NULL,
  num_bedrooms INT NOT NULL,
  num_bathrooms INT NOT NULL,
  is_guest_favourite BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- bookings
CREATE TABLE IF NOT EXISTS bookings (
  booking_id BIGSERIAL PRIMARY KEY,
  property_id BIGINT NOT NULL REFERENCES property(property_id) ON DELETE CASCADE,
  user_id BIGINT NOT NULL REFERENCES user_account(id) ON DELETE CASCADE,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  total_price DECIMAL(10,2) NOT NULL,
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- guest_type
CREATE TABLE IF NOT EXISTS guest_type (
  guest_type_id SERIAL PRIMARY KEY,
  type_name VARCHAR(255) NOT NULL
);

-- booking_guests
CREATE TABLE IF NOT EXISTS booking_guests (
  booking_id BIGINT NOT NULL REFERENCES bookings(booking_id) ON DELETE CASCADE,
  guest_type_id INT NOT NULL REFERENCES guest_type(guest_type_id),
  num_guests INT NOT NULL,
  PRIMARY KEY (booking_id, guest_type_id)
);

-- user_review
CREATE TABLE IF NOT EXISTS user_review (
  review_id BIGSERIAL PRIMARY KEY,
  property_id BIGINT NOT NULL REFERENCES property(property_id) ON DELETE CASCADE,
  user_id BIGINT NOT NULL REFERENCES user_account(id) ON DELETE CASCADE,
  booking_id BIGINT REFERENCES bookings(booking_id),
  overall_rating INT NOT NULL,
  comment TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- review_component
CREATE TABLE IF NOT EXISTS review_component (
  review_component_id SERIAL PRIMARY KEY,
  component_name VARCHAR(255) NOT NULL
);

-- component_rating
CREATE TABLE IF NOT EXISTS component_rating (
  component_id BIGSERIAL PRIMARY KEY,
  review_id BIGINT NOT NULL REFERENCES user_review(review_id) ON DELETE CASCADE,
  review_component_id INT NOT NULL REFERENCES review_component(review_component_id),
  rating INT NOT NULL
);

-- conversation
CREATE TABLE IF NOT EXISTS conversation (
  conversation_id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- conversation_participants
CREATE TABLE IF NOT EXISTS conversation_participants (
  conversation_id BIGINT NOT NULL REFERENCES conversation(conversation_id) ON DELETE CASCADE,
  user_id BIGINT NOT NULL REFERENCES user_account(id) ON DELETE CASCADE,
  PRIMARY KEY (conversation_id, user_id)
);

-- favourite
CREATE TABLE IF NOT EXISTS favourite (
  user_account_id BIGINT NOT NULL REFERENCES user_account(id) ON DELETE CASCADE,
  property_id BIGINT NOT NULL REFERENCES property(property_id) ON DELETE CASCADE,
  PRIMARY KEY (user_account_id, property_id)
);

-- language
CREATE TABLE IF NOT EXISTS language (
  language_id SERIAL PRIMARY KEY,
  language VARCHAR(255) NOT NULL
);

-- payment
CREATE TABLE IF NOT EXISTS payment (
  payment_id BIGSERIAL PRIMARY KEY,
  booking_id BIGINT NOT NULL REFERENCES bookings(booking_id) ON DELETE CASCADE,
  amount DECIMAL(10,2) NOT NULL,
  payment_date TIMESTAMP,
  payment_method VARCHAR(100),
  paid_at TIMESTAMP
);

-- property_attribute
CREATE TABLE IF NOT EXISTS property_attribute (
  property_id BIGINT NOT NULL REFERENCES property(property_id) ON DELETE CASCADE,
  attribute_id INT NOT NULL REFERENCES attribute(attribute_id) ON DELETE CASCADE,
  PRIMARY KEY (property_id, attribute_id)
);

-- property_images
CREATE TABLE IF NOT EXISTS property_images (
  image_id BIGSERIAL PRIMARY KEY,
  property_id BIGINT NOT NULL REFERENCES property(property_id) ON DELETE CASCADE,
  image_url VARCHAR(500) NOT NULL,
  image_order INT DEFAULT 0
);

-- roles
CREATE TABLE IF NOT EXISTS roles (
  id SERIAL PRIMARY KEY,
  name VARCHAR(20) NOT NULL UNIQUE CHECK (name IN ('host', 'guest', 'admin'))
);

-- user_language
CREATE TABLE IF NOT EXISTS user_language (
  user_language_id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES user_account(id) ON DELETE CASCADE,
  language_id INT NOT NULL REFERENCES language(language_id)
);

-- user_roles
CREATE TABLE IF NOT EXISTS user_roles (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES user_account(id) ON DELETE CASCADE,
  role_id INT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
  UNIQUE (user_id, role_id)
);
