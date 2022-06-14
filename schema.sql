CREATE TABLE videos (

    file_name TEXT PRIMARY KEY NOT NULL,
    
    file_path TEXT,
    
    train_path TEXT,
    
    original_collection TEXT,
    
    original_title TEXT,
    
    title_en TEXT,
    
    year INT,
    
    date TEXT,
    
    armed_groups TEXT,
    
    adm1 TEXT,
    
    adm2 TEXT,
    
    adm3 TEXT,
    
    adm4 TEXT,
    
    place_name TEXT,
    
    is_training BOOL,
    
    is_indexed BOOL,
    
    vi_id TEXT,
    
    insights TEXT,
    
    pred_results TEXT
);