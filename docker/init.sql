CREATE TABLE image1_features (
    id SERIAL PRIMARY KEY,
    area DOUBLE PRECISION,
    perimeter DOUBLE PRECISION,
    aspect_ratio DOUBLE PRECISION,
    solidity DOUBLE PRECISION,
    circularity DOUBLE PRECISION,
    orientation DOUBLE PRECISION,
    hu_moments DOUBLE PRECISION[],
    histogram DOUBLE PRECISION[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE image2_features (LIKE image1_features INCLUDING ALL);
CREATE TABLE image3_features (LIKE image1_features INCLUDING ALL);
