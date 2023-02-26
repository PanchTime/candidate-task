CREATE DATABASE IF NOT EXISTS investments;

USE investments;

DROP TABLE IF EXISTS `fund`;
DROP TABLE IF EXISTS `share_class`;
DROP TABLE IF EXISTS `price`;
DROP TABLE IF EXISTS `return`;
DROP TABLE IF EXISTS `dividend`;
DROP TABLE IF EXISTS `net_asset`;

CREATE TABLE fund (
	fund_id INTEGER NOT NULL AUTO_INCREMENT,
	category_id INTEGER,
	primary_index_id INTEGER,
	secondary_index_id INTEGER,
	prospectus_objective_id INTEGER,
	oldest_share_class INTEGER,
	PRIMARY KEY (fund_id)
);

CREATE TABLE share_class (
	share_class_id INTEGER NOT NULL AUTO_INCREMENT,
	fund_id INTEGER,
	shareclass_name VARCHAR(255),
	legal_type VARCHAR(255),
	cusip VARCHAR(255),
	ticker VARCHAR(255),
	isin VARCHAR(255),
	inception_date DATE,
	currency VARCHAR(255),
	PRIMARY KEY (share_class_id),
);

CREATE TABLE price (
    price_id INTEGER NOT NULL AUTO_INCREMENT,
    share_class_id INTEGER,
    price_type INTEGER
    end_date DATE,
    close_price DECIMAL(15,5),
    PRIMARY KEY (price_id)
);


CREATE TABLE return (
    return_id INTEGER NOT NULL AUTO_INCREMENT,
    share_class_id INTEGER,
    store_date DATE,
    end_date DATE,
    time_period VARCHAR(255),
    return_type INTEGER,
    return_value DECIMAL(15,5),
    PRIMARY KEY (return_id)
);

CREATE TABLE dividend (
    dividend_id INTEGER NOT NULL AUTO_INCREMENT,
    share_class_id INTEGER,
    excluding_date DATE,
    reinvesting_date DATE,
    total_dividend DECIMAL(15,4),
    non_qualified_dividend DECIMAL(15,4),
    PRIMARY KEY (dividend)
);

CREATE TABLE capital_gain (
    capital_gain_id INTEGER NOT NULL AUTO_INCREMENT,
    share_class_id INTEGER,
    excluding_date DATE,
    reinvest_date DATE,
    long_term_gain DECIMAL(15,4),
    total_capital_gain DECIMAL(15,4),
    PRIMARY KEY (capital_gain_id)
);


CREATE TABLE net_asset (
    operation_id INTEGER NOT NULL AUTO_INCREMENT,
    share_class_id INTEGER,
    end_date DATE,
    value DECIMAL(15,2),
    PRIMARY KEY (operation_id)
);
