Utilities to create csv toc file for use with MobileSheets application

Use the notebook and find this example example
Example in the notebook

Set location and names
```
fname = 'The Beatles Complete - Vol 1 A-I.csv'
dlmtr = ","
output_dir = '/usr/local/dev/MuApi/SheetMusicIndices/indexes'
input_dir = '/usr/local/dev/MuApi/SheetMusicIndices/origindex/'

abbrv = "[BCV1]"
collections = 'The Beatles Complete'
genres = 'Rock|Pop'
composers = "Lennon/Mcartney, George Harrison"
pdf_file = "/home/mike/Documents/tunes/Beatles/Beatles/The Beatles Complete - Vol 1 A-I.pdf"
```

The abreviation is to differentiate files in you Mobile Sheets library. If you have multiple version of songs for example from Real Book 1 and New RealBook 1, they can lool like this:

"All of Me"  (RB1)

"All of Me"  (NRB1)


If the pdf has toc info extract it 

```

csv_file = os.path.join(input_dir, fname)
save_toc_to_csv(pdf_file, csv_file)
total_pages = get_page_count(pdf_file)
total_pages
```

Create the index
```
ms = MobileIndex(
    fname,
    dlmtr,
    output_dir,
    input_dir,
    total_pages,
    abbrv=abbrv,
    genres=genres,
    collections=collections,
    composers=composers,
)

ms.write_csv()
```

