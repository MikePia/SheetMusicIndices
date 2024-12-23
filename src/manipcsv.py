import logging
import csv
import os
import re
import string
import sys

logger = logging.getLogger(__name__)


class MobileIndex:
    fname = ''
    outdir = 'indexes'
    outfile = ''
    dlmtr = ';'
    newcsv = []
    abbrv = ' (NRB1)'
    collection = None
    genres = None
    maxval = 999999
    begin = None
    offset = None
    capb = 0

    def __init__(self, fname, abbrv, dlmtr=';', collection=None, genres=None, offset=None, capb=0, composers= None):
        self.fname = fname

        if not os.path.exists(self.fname):
            print('Error, file does not exist: EXITING')
            sys.exit(1)
        self.abbrv = abbrv
        self.dlmtr = dlmtr
        self.capb = capb
        if collection:
            if isinstance(collection, str):
                self.collections = [collection]
            elif isinstance(collection, list):
                self.collections = collection
            coll = self.collections[0]
            for i in range(1, len(collection)):
                coll += '|'
                coll += self.collections[i]
            self.collections = coll
        if genres:
            if isinstance(genres, str):
                self.genres = [genres]
            elif isinstance(genres, list):
                self.genres = genres
                gen = self.genres[0]
                for i in range(1, len(self.genres)):
                    gen += '|'
                    gen += self.genres[i]
                self.genres = gen

        if not os.path.exists(fname):
            logger.error(f'Filename {fname} cannot be located')
            logger.error('Exiting program')
            sys.exit(1)
        self.setoutname()
        if offset:
            self.begin = offset[0]
            self.offset = offset[1]
        if composers:
            self.composers = composers

    def create_index(self):

        with open(self.fname) as csvfile:
            reader = csv.reader(csvfile, delimiter=self.dlmtr)
            header = None
            titleindex = -1
            cindex = -1
            for row in reader:
                if header is None:
                    # Read the header and set up static data
                    _header = row
                    header = [x.lower() for x in _header]
                    if 'title' not in header:
                        if len(header) < 2:
                            logger.error(f'Cannot read the file. Maybe the wrong delimiter is set "{self.dlmtr}"')
                        else:
                            logger.error("Input file does not have a title header")
                        logger.error('Exiting program')
                        sys.exit(1)

                    titleindex = header.index('title')
                    cindex = -1
                    if self.collections:
                        if 'collections' in header:
                            cindex = header.index('collections')
                        else:
                            row.append('collections')
                            cindex = self.maxval
                    gindex = -1
                    if self.genres:
                        if 'genres' in header:
                            gindex = header.index('genres')
                        else:
                            row.append('genres')
                            gindex = self.maxval

                    if self.composers:
                        if 'composers' in header:
                            self.compindex = header.index('composers')
                        else:
                            row.append('composers')
                            header.append('composers')
                            self.compindex = header.index('composers')
                        
                    oindex = -1
                    if self.offset:
                        oindex = header.index('pages')

                else:
                    # Create the entries
                    if self.capb:
                        row[titleindex] = string.capwords(row[titleindex])
                    # Check for an empty line
                    if not row:
                        continue
                    row[titleindex] = f'{row[titleindex].strip()} {self.abbrv}'
                    row[titleindex] = re.sub(' +', ' ', row[titleindex])
                    if self.collections:
                        if cindex == self.maxval:
                            row.append(self.collections)
                        else:
                            row[cindex] = self.collections
                    if self.genres:
                        if gindex == self.maxval:
                            row.append(self.genres)
                        else:
                            row[gindex] = self.genres
                    if self.composers:
                        if self.compindex == self.maxval:
                            row.appendindex = self.composers
                        else:
                            row[self.compindex] = self.composers
                    
                    
                    if self.offset:
                        # Offset pages by the value in self.offset beginning at self.begin
                        pages = row[oindex].split('-')
                        pages = [int(x) for x in pages]
                        if pages[-1] >= self.begin:
                            offsetpages = [x + self.offset for x in pages]

                            if len(offsetpages) == 1:
                                row[oindex] = str(offsetpages[0])
                            else:
                                assert len(offsetpages) == 2
                                row[oindex] = f'{offsetpages[0]}-{offsetpages[1]}'

                        print()
                    # for coll in self.collections:
                    #      += coll
                self.newcsv.append(row)

    def create_new_index(self):
        with open(self.outfile, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=self.dlmtr)
            for row in self.newcsv:
                writer.writerow(row)

    def setoutname(self):
        _, renameorig = os.path.split(self.fname)
        self.outfile = os.path.join(self.outdir, f'{renameorig}')

        return self.outfile

    def calcEnd(self):
        with open(self.fname) as csvfile:
            reader = csv.reader(csvfile, delimiter=self.dlmtr)
            header = None
            titleindex = -1
            pageindex = -1
            currentrow = None
            nextrow = None
            thisisthealbum = False

            for row in reader:
                thisisthealbum = False
                if header is None:
                    _header = row
                    header = [x.lower() for x in _header]
                    pageindex = header.index('pages')
                    self.newcsv.append(row)
                    continue
                else:
                    pagenumber = row[pageindex]
                    pagenumber = pagenumber.split('-')
                    if len(pagenumber) > 1:
                        thisisthealbum = True

                    pagenumber = int(pagenumber[0])
                    if not currentrow:
                        currentrow = row
                        currentpage = pagenumber
                        continue
                    nextrow = row
                    nextpage = pagenumber
                    
                    addthisrow = currentrow
                    addthisrow[pageindex] = f'{currentpage}-{nextpage-1}'
                    
                    currentrow = nextrow
                    currentpage = pagenumber
                        
                    print()
                self.newcsv.append(addthisrow)
        self.setoutname()
        self.create_new_index()


if __name__ == '__main__':
    testfname = 'origindex/steely-dan-complete.csv'
    abrev = '(SDC)'
    collection = ['Steely Dan Complete']
    genres = ['Pop']
    offset = [1,9]
    composers = "Becker, Walter &, Fagen, Donald"

    ms = MobileIndex(testfname, abrev,
                     collection=collection,
                     genres=genres,
                     offset=offset,
                     composers = composers
                     )
    ms.calcEnd()
    # ms.create_index()
    # ms.create_new_index()
    print("done")
