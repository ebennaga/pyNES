class Cartridge:

    def __init__(self):
        self.banks = {}
        self.bank_id = 0
        self.pc = 0
        self.inespgr = 1
        self.ineschr = 1
        self.inesmap = 1
        self.inesmir = 1

    def nes_id(self):
        #NES 
        return [0x4e, 0x45, 0x53, 0x1a]

    def nes_get_header(self):
        id = self.nes_id();
        unused = [0,0,0,0,0,0,0,0]
        header = []
        header.extend(id)
        header.append(self.inespgr)
        header.append(self.ineschr)
        header.append(self.inesmir)
        header.append(self.inesmap)
        header.extend(unused)
        return header

    def set_iNES_prg(self, inespgr):
        self.inespgr = inespgr

    def set_iNES_chr(self, ineschr):
        self.ineschr = ineschr

    def set_iNES_map(self, inesmap):
        self.inesmap = inesmap

    def set_iNES_mir(self, inesmir):
        self.inesmir = inesmir

    def set_bank_id(self, id):
        if id not in self.banks:
            self.banks[id] = dict(code=[], start=None, size=(1024*8))
        self.bank_id = id

    def set_org(self, org):
        if self.bank_id not in self.banks:
            self.set_bank_id(self.bank_id)
        if not self.banks[self.bank_id]['start']:
            self.banks[self.bank_id]['start'] = org
            self.pc = org
        else:
            while self.pc < org:
                self.append_code([0xff])
            self.pc = org

    def append_code(self, code):
        if self.bank_id not in self.banks:
            self.set_bank_id(self.bank_id)
        for c in code:
            assert c <= 0xff
        self.banks[self.bank_id]['code'].extend(code)
        self.pc += len(code)

    def get_code(self):
        if self.bank_id not in self.banks:
            self.set_bank_id(self.bank_id)
        return self.banks[self.bank_id]['code']

    def get_ines_code(self):
        if self.bank_id not in self.banks:
            self.set_bank_id(self.bank_id)
        bin = []
        nes_header = self.nes_get_header()
        for i in range(len(self.banks[0]['code']), self.banks[0]['size']):
            self.banks[0]['code'].append(0xff)
        bin.extend(nes_header)
        bin.extend(self.banks[0]['code'])
        if 1 in self.banks:
            for i in range(len(self.banks[1]['code']), 1024*8):
                self.banks[1]['code'].append(0xff)
            bin.extend(self.banks[1]['code'])
        if 2 in self.banks:
            bin.extend(self.banks[2]['code'])
        return bin
