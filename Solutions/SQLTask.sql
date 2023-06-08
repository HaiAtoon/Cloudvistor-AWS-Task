--	================
--	| Answer No. 1 |
--	================

-- Creating table for regions

CREATE TABLE regions (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Inserting data to 'regions' table
INSERT INTO regions (id, name)
VALUES 
    (1, 'Northeast'),
    (2, 'Midwest'),
    (3, 'South'),
    (4, 'West');

-- Creating table for markets

CREATE TABLE markets (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    region_id INT NOT NULL,
    FOREIGN KEY (region_id) REFERENCES regions(id)
);

-- Inserting data to 'markets' table

INSERT INTO markets (id, name, region_id)
VALUES 
    (1, 'New York City', 1),
    (2, 'Chicago', 2),
    (3, 'Dallas', 3),
    (4, 'Los Angeles', 4);

-- Creating table for states

CREATE TABLE states (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    region_id INT NOT NULL,
    FOREIGN KEY (region_id) REFERENCES regions(id)
);

-- Inserting data to 'states' table

INSERT INTO states (id, name, region_id)
VALUES 
    (1, 'New York', 1),
    (2, 'Illinois', 2),
    (3, 'Texas', 3),
    (4, 'California', 4);

-- Creating table for submarkets

CREATE TABLE submarkets (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    market_id INT NOT NULL,
    FOREIGN KEY (market_id) REFERENCES markets(id)
);

-- Inserting data to 'submarkets' table

INSERT INTO submarkets (id, name, market_id)
VALUES 
    (1, 'Manhattan', 1),
    (2, 'Queens', 1),
    (3, 'Bronx', 1),
    (4, 'Brooklyn', 1),
    (5, 'Staten Island', 1);

-- Creating table for polygons

CREATE TABLE polygons (
    id INT PRIMARY KEY,
    submarket_id INT NOT NULL,
    polygon GEOMETRY NOT NULL,
    FOREIGN KEY (submarket_id) REFERENCES submarkets(id)
);

-- Inserting data to 'polygons' table

INSERT INTO polygons (id, submarket_id, polygon)
VALUES 
    (1, 1, ST_GeomFromText('POLYGON((40.697670 -74.259870, 40.698210 -74.251840, 40.695320 -74.248410, 40.693410 -74.256440, 40.697670 -74.259870))')),
    (2, 2, ST_GeomFromText('POLYGON((40.744060 -73.835400, 40.756820 -73.807460, 40.711920 -73.736100, 40.698160 -73.764040, 40.744060 -73.835400))')),
    (3, 3, ST_GeomFromText('POLYGON((40.899620 -73.911000, 40.896910 -73.896210, 40.858430 -73.902030, 40.861150 -73.916820, 40.899620 -73.911000))')),
    (4, 4, ST_GeomFromText('POLYGON((40.800210 -73.935280, 40.779640 -73.876210, 40.737140 -73.896210, 40.757710 -73.955280, 40.800210 -73.935280))')),
    (5, 5, ST_GeomFromText('POLYGON((40.578460 -74.146590, 40.564820 -74.121110, 40.526330 -74.136840, 40.539970 -74.162660, 40.578460 -74.146590))'));


--	================
--	| Answer No. 2 |
--	================

--If the product team can only provide polygons that match the market and not the submarkets, the database would need to be adjusted to include a mapping table between markets and submarkets. 
--The mapping table would have two columns, one for the market ID and one for the submarket ID. 
--This way, I will be able to join the polygons table to the mapping table to get the submarket ID, and then to join the submarkets table and get the submarket name. 
--My query would look like this:

-- Query to get submarket, market, state, and region based on address and coordinates

SELECT 
    sub.name AS submarket_name,
    mkt.name AS market_name,
    st.name AS state_name,
    reg.name AS region_name
    FROM 
    polygons p 
    INNER JOIN submarkets sub ON p.submarket_id = sub.id
    INNER JOIN markets mkt ON sub.market_id = mkt.id    
    INNER JOIN states st ON mkt.region_id = st.region_id    
    INNER JOIN regions reg ON st.region_id = reg.id
    WHERE 
    ST_Within(ST_GeomFromText('POINT(-73.799700 40.718800)'), p.polygon);

-- *** I Replace coordinates in the ST_GeomFromText function with the coordinates of the address ***


-- The market_submarket_map table would have two columns:

CREATE TABLE market_submarket_map (
    market_id INT NOT NULL,
    submarket_id INT NOT NULL,
    PRIMARY KEY (market_id, submarket_id),
    FOREIGN KEY (market_id) REFERENCES markets(id),
    FOREIGN KEY (submarket_id) REFERENCES submarkets(id)
);

-- I would also need to update the INSERT statements for the polygons table to include the market ID instead of the submarket ID.

