CREATE TABLE auction_imports (
  id INTEGER NOT NULL AUTO_INCREMENT,
  url VARCHAR(255),
  realm VARCHAR(255),
  lastModified BIGINT UNSIGNED,
  PRIMARY KEY (id)
);

CREATE TABLE auction_data (
  auc BIGINT UNSIGNED NOT NULL,
  item BIGINT UNSIGNED,
  owner VARCHAR(255),
  ownerRealm VARCHAR(255),
  bid INT UNSIGNED,
  buyout INT UNSIGNED,
  quantity INT UNSIGNED,
  timeLeft VARCHAR(50),
  rand INT UNSIGNED,
  seed INT UNSIGNED,
  context INT UNSIGNED,
  import_id INTEGER NOT NULL,
  PRIMARY KEY (auc)
);
