DROP TABLE IF EXISTS slides;
DROP TABLE IF EXISTS BOXES;
CREATE TABLE BOXES (
  TR_ID SERIAL NOT NULL PRIMARY KEY,    /* Table row ID */
  TS NUMERIC, 
  BOX_ID TEXT NOT NULL UNIQUE,          /* Need to find out string length */
  CABINET_ID TEXT UNIQUE
);
CREATE TABLE slides (
  SlideID TEXT NOT NULL PRIMARY KEY,                         /* Need to find out string length */
  BlockID TEXT,
  AccessionID TEXT,
  Stain TEXT,
  StainOrderDate TIMESTAMP,
  SiteLabel TEXT,
  CaseType TEXT,
  Year VARCHAR(4),
  TS NUMERIC,
  LOCATION TEXT,
  RetrievalRequest BOOLEAN,
  RequestedBy  TEXT,
  RequestTS Numeric,                        /* 100 slots per box */
  BOX_ID TEXT,
  CONSTRAINT box_constraint
  FOREIGN KEY (BOX_ID)
  REFERENCES BOXES (BOX_ID)
);
