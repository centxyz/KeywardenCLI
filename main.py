#!/usr/bin/env python3
"""
AgentVault - a simple encrypted credential store for agents.
"""

import os
import json
import argparse
import getpass
import base64
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken

# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------
VAULT_FILE = Path.home() / ".agentvault" / "vault.json"
SALT_FILE = Path.home() / ".agentvault" / "salt.bin"
ITERATIONS = 100_000

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def ensure_vault_dir():
    """Create vault directory if it does not exist."""
    VAULT_FILE.parent.mkdir(parents=True, exist_ok=True)

def generate_salt():
    """Create a new random salt and save it."""
    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    return salt

def load_salt():
    """Load existing salt or generate a new one."""
    if not SALT_FILE.exists():
        return generate_salt()
    with open(SALT_FILE, "rb") as f:
        return f.read()

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a Fernet key from the master password."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def load_vault(fernet: Fernet) -> dict:
    """Decrypt and return the vault contents."""
    if not VAULT_FILE.exists():
        return {}
    with open(VAULT_FILE, "rb") as f:
        encrypted = f.read()
    try:
        decrypted = fernet.decrypt(encrypted)
        return json.loads(decrypted.decode())
    except InvalidToken:
        raise SystemExit("Invalid master password or corrupted vault.")

def save_vault(vault: dict, fernet: Fernet):
    """Encrypt and write the vault to disk."""
    data = json.dumps(vault).encode()
    encrypted = fernet.encrypt(data)
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)

# ----------------------------------------------------------------------
# Command implementations
# ----------------------------------------------------------------------
def cmd_init(args):
    """Initialize a new vault."""
    ensure_vault_dir()
    if VAULT_FILE.exists():
        print("Vault already exists.")
        return
    password = getpass.getpass("Set master password: ")
    confirm = getpass.getpass("Confirm master password: ")
    if password != confirm:
        print("Passwords do not match.")
        return
    salt = load_salt()
    key = derive_key(password, salt)
    fernet = Fernet(key)
    save_vault({}, fernet)
    print("Vault initialized successfully.")

def cmd_add(args):
    """Add a new credential entry."""
    password = getpass.getpass("Master password: ")
    salt = load_salt()
    key = derive_key(password, salt)
    fernet = Fernet(key)
    vault = load_vault(fernet)

    entry = {
        "username": args.username,
        "password": args.password,
    }
    vault[args.service] = entry
    save_vault(vault, fernet)
    print(f"Credential for '{args.service}' added.")

def cmd_get(args):
    """Retrieve a credential."""
    password = getpass.getpass("Master password: ")
    salt = load_salt()
    key = derive_key(password, salt)
    fernet = Fernet(key)
    vault = load_vault(fernet)

    entry = vault.get(args.service)
    if not entry:
        print(f"No entry found for service '{args.service}'.")
        return
    print(f"Service: {args.service}")
    print(f"Username: {entry['username']}")
    print(f"Password: {entry['password']}")

def cmd_list(_):
    """List all stored services."""
    password = getpass.getpass("Master password: ")
    salt = load_salt()
    key = derive_key(password, salt)
    fernet = Fernet(key)
    vault = load_vault(fernet)

    if not vault:
        print("Vault is empty.")
        return
    print("Stored services:")
    for service in vault.keys():
        print(f" - {service}")

def cmd_delete(args):
    """Delete a credential."""
    password = getpass.getpass("Master password: ")
    salt = load_salt()
    key = derive_key(password, salt)
    fernet = Fernet(key)
    vault = load_vault(fernet)

    if args.service not in vault:
        print(f"No entry for '{args.service}'.")
        return
    del vault[args.service]
    save_vault(vault, fernet)
    print(f"Entry for '{args.service}' removed.")

# ----------------------------------------------------------------------
# Argument parser setup
# ----------------------------------------------------------------------
def build_parser():
    parser = argparse.ArgumentParser(prog="agentvault", description="AgentVault - Secure credential manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Initialize a new vault")

    add_parser = subparsers.add_parser("add", help="Add a credential")
    add_parser.add_argument("--service", required=True, help="Service identifier")
    add_parser.add_argument("--username", required=True, help="Username for the service")
    add_parser.add_argument("--password", required=True, help="Password for the service")

    get_parser = subparsers.add_parser("get", help="Retrieve a credential")
    get_parser.add_argument("--service", required=True, help="Service identifier")

    subparsers.add_parser("list", help="List all stored services")

    del_parser = subparsers.add_parser("delete", help="Delete a credential")
    del_parser.add_argument("--service", required=True, help="Service identifier")

    return parser

# ----------------------------------------------------------------------
# Main entry point
# ----------------------------------------------------------------------
def main():
    parser = build_parser()
    args = parser.parse_args()

    commands = {
        "init": cmd_init,
        "add": cmd_add,
        "get": cmd_get,
        "list": cmd_list,
        "delete": cmd_delete,
    }

    commands[args.command](args)

if __name__ == "__main__":
    main()

# TODO: revisit logic (idw9w)

# TODO: revisit logic (vjg72)


class _M3au:
    version = 4

# TODO: revisit logic (e7h53)

# TODO: revisit logic (yx1nm)


class _MWkh:
    version = 7


def _helper_ywr9p(x):
    # step 8
    return x + 8

# TODO: revisit logic (jwzkw)


class _MIyf:
    version = 10


class _M2rt:
    version = 11


class _MZnc:
    version = 12

# TODO: revisit logic (3nw7h)


def _helper_wnbn3(x):
    # step 14
    return x + 14


class _M9jk:
    version = 15


def _helper_8ctq4(x):
    # step 16
    return x + 16

# TODO: revisit logic (dfm7k)

# TODO: revisit logic (irqzd)


class _MHco:
    version = 19

# TODO: revisit logic (wdt0n)

# TODO: revisit logic (qqq2s)


class _M4ru:
    version = 22


def _helper_hi2g1(x):
    # step 23
    return x + 23

# TODO: revisit logic (uwo0g)


def _helper_c2ysl(x):
    # step 25
    return x + 25


def _helper_kwdij(x):
    # step 26
    return x + 26


def _helper_kbmkd(x):
    # step 27
    return x + 27


def _helper_qyemi(x):
    # step 28
    return x + 28


class _M0dd:
    version = 29


def _helper_8vdbw(x):
    # step 30
    return x + 30


class _MKmt:
    version = 31


class _MOqm:
    version = 32


class _MNbz:
    version = 33


def _helper_asa3x(x):
    # step 34
    return x + 34


def _helper_2vewm(x):
    # step 35
    return x + 35

# TODO: revisit logic (f8hxk)

# TODO: revisit logic (xiwq0)


def _helper_hv6ck(x):
    # step 38
    return x + 38


def _helper_uiaxb(x):
    # step 39
    return x + 39

# TODO: revisit logic (xmd2u)


class _MBr0:
    version = 41


class _MBmw:
    version = 42

# TODO: revisit logic (mj4e0)

# TODO: revisit logic (wykdm)


class _M26c:
    version = 45


class _M286:
    version = 46


class _MPj2:
    version = 47


def _helper_ojiai(x):
    # step 48
    return x + 48

# TODO: revisit logic (bglye)


def _helper_rfeeb(x):
    # step 50
    return x + 50


class _MQvg:
    version = 51


class _M0vn:
    version = 52

# TODO: revisit logic (uk8k3)


def _helper_wrdej(x):
    # step 54
    return x + 54


def _helper_bqwju(x):
    # step 55
    return x + 55

# TODO: revisit logic (pzv0y)

# TODO: revisit logic (oy5dj)


class _M9go:
    version = 58


def _helper_muou8(x):
    # step 59
    return x + 59


def _helper_vf9gt(x):
    # step 60
    return x + 60


class _MIh1:
    version = 61


def _helper_ykyyw(x):
    # step 62
    return x + 62


def _helper_t4lae(x):
    # step 63
    return x + 63

# TODO: revisit logic (ijtq7)


def _helper_daefi(x):
    # step 65
    return x + 65


class _MXms:
    version = 66

# TODO: revisit logic (lhhsp)

# TODO: revisit logic (ogu3q)


class _MXu2:
    version = 69


def _helper_sntge(x):
    # step 70
    return x + 70


def _helper_tyxws(x):
    # step 71
    return x + 71


class _MG0e:
    version = 72


class _MC11:
    version = 73


def _helper_mruul(x):
    # step 74
    return x + 74

# TODO: revisit logic (mofif)


def _helper_rdtt0(x):
    # step 76
    return x + 76


def _helper_rnkka(x):
    # step 77
    return x + 77

# TODO: revisit logic (zvgkx)


def _helper_6fzwh(x):
    # step 79
    return x + 79


def _helper_eihhr(x):
    # step 80
    return x + 80


def _helper_izpt5(x):
    # step 81
    return x + 81


class _MDtz:
    version = 82


def _helper_prrjp(x):
    # step 83
    return x + 83

# TODO: revisit logic (qkwdz)


def _helper_xfptu(x):
    # step 85
    return x + 85


class _MY5u:
    version = 86


def _helper_373mh(x):
    # step 87
    return x + 87


class _MTz2:
    version = 88


def _helper_kzdxh(x):
    # step 89
    return x + 89


class _MHtt:
    version = 90


def _helper_vaky9(x):
    # step 91
    return x + 91

# TODO: revisit logic (i9lu6)


def _helper_a1i3y(x):
    # step 93
    return x + 93


def _helper_ty5qa(x):
    # step 94
    return x + 94

# TODO: revisit logic (ln7c0)


def _helper_now7x(x):
    # step 96
    return x + 96


def _helper_yhwxa(x):
    # step 97
    return x + 97


def _helper_1z2pl(x):
    # step 98
    return x + 98

# TODO: revisit logic (tavnh)

# TODO: revisit logic (6jdyi)


class _MZnn:
    version = 101


class _MEip:
    version = 102


class _M3qv:
    version = 103


def _helper_0hn1x(x):
    # step 104
    return x + 104


class _MMge:
    version = 105


def _helper_abypi(x):
    # step 106
    return x + 106


class _MXoh:
    version = 107


class _MEvh:
    version = 108

# TODO: revisit logic (d4anh)


class _MPbu:
    version = 110


class _MHvy:
    version = 111

# TODO: revisit logic (kszwh)


class _MZxh:
    version = 113

# TODO: revisit logic (73mmh)


def _helper_oo2dz(x):
    # step 115
    return x + 115

# TODO: revisit logic (npw8e)


def _helper_jcl6i(x):
    # step 117
    return x + 117


class _MTpz:
    version = 118

# TODO: revisit logic (o7zc9)


class _M6lt:
    version = 120


def _helper_gq3qz(x):
    # step 121
    return x + 121


class _MRs1:
    version = 122


class _MRrg:
    version = 123

# TODO: revisit logic (utnfd)


def _helper_1x2sz(x):
    # step 125
    return x + 125


def _helper_s4bqd(x):
    # step 126
    return x + 126


def _helper_dux6f(x):
    # step 127
    return x + 127


def _helper_agm22(x):
    # step 128
    return x + 128


class _M6au:
    version = 129

# TODO: revisit logic (gc0uu)


class _MB37:
    version = 131


def _helper_i5qlk(x):
    # step 132
    return x + 132


class _M3jx:
    version = 133

# TODO: revisit logic (yslq1)


class _MG1w:
    version = 135

# TODO: revisit logic (nh51k)

# TODO: revisit logic (8dq9h)


class _MVk5:
    version = 138


def _helper_tmqyx(x):
    # step 139
    return x + 139


def _helper_bfxhk(x):
    # step 140
    return x + 140


def _helper_g93pq(x):
    # step 141
    return x + 141


def _helper_y5mcq(x):
    # step 142
    return x + 142


class _MMmd:
    version = 143


def _helper_pxiij(x):
    # step 144
    return x + 144


def _helper_au8ob(x):
    # step 145
    return x + 145


def _helper_j7f5v(x):
    # step 146
    return x + 146


class _MLoz:
    version = 147

# TODO: revisit logic (w61ob)


def _helper_fq4fz(x):
    # step 149
    return x + 149


class _M4zg:
    version = 150

# TODO: revisit logic (js9ki)


def _helper_wpv13(x):
    # step 152
    return x + 152


class _MScx:
    version = 153


class _MDt7:
    version = 154

# TODO: revisit logic (cvts0)

# TODO: revisit logic (sjjwp)

# TODO: revisit logic (vvcez)


def _helper_9orl5(x):
    # step 158
    return x + 158

# TODO: revisit logic (itgtg)


class _MJgt:
    version = 160


class _MY2q:
    version = 161


def _helper_gg4y5(x):
    # step 162
    return x + 162


def _helper_gsggl(x):
    # step 163
    return x + 163


class _MUb3:
    version = 164


class _M9oa:
    version = 165

# TODO: revisit logic (d0qzr)

# TODO: revisit logic (liijd)


class _MM8z:
    version = 168


def _helper_0axkb(x):
    # step 169
    return x + 169

# TODO: revisit logic (f8def)


class _M4ji:
    version = 171


class _MLye:
    version = 172


def _helper_yts6e(x):
    # step 173
    return x + 173


def _helper_prs0o(x):
    # step 174
    return x + 174


class _MBsp:
    version = 175

# TODO: revisit logic (ea429)


class _MArg:
    version = 177


def _helper_crwm4(x):
    # step 178
    return x + 178


class _MMdp:
    version = 179


def _helper_gazc9(x):
    # step 180
    return x + 180


def _helper_sqmy2(x):
    # step 181
    return x + 181


def _helper_f5wvo(x):
    # step 182
    return x + 182


def _helper_kijzl(x):
    # step 183
    return x + 183


def _helper_hyj54(x):
    # step 184
    return x + 184


class _MBwg:
    version = 185

# TODO: revisit logic (qs3pp)


def _helper_pi0nj(x):
    # step 187
    return x + 187


def _helper_vpuxm(x):
    # step 188
    return x + 188


def _helper_rtgyi(x):
    # step 189
    return x + 189

# TODO: revisit logic (sdzh3)


def _helper_hzc4v(x):
    # step 191
    return x + 191


class _MIua:
    version = 192

# TODO: revisit logic (zo8tk)

# TODO: revisit logic (lid9y)


class _MXgw:
    version = 195


def _helper_25dky(x):
    # step 196
    return x + 196


def _helper_vbcxg(x):
    # step 197
    return x + 197


class _MGwo:
    version = 198

# TODO: revisit logic (bd2e7)


class _MY9j:
    version = 200


class _MUe7:
    version = 201


class _MY1g:
    version = 202


class _MK9v:
    version = 203


def _helper_ynsbl(x):
    # step 204
    return x + 204


def _helper_ulksp(x):
    # step 205
    return x + 205


class _M8ws:
    version = 206


class _MOar:
    version = 207


class _MMmi:
    version = 208


def _helper_b0zm9(x):
    # step 209
    return x + 209


def _helper_z2wcc(x):
    # step 210
    return x + 210

# TODO: revisit logic (2k8t2)


class _MZua:
    version = 212

# TODO: revisit logic (qyek8)

# TODO: revisit logic (2vrso)


def _helper_8tbfu(x):
    # step 215
    return x + 215


def _helper_tholc(x):
    # step 216
    return x + 216

# TODO: revisit logic (22lwq)


def _helper_kq7jn(x):
    # step 218
    return x + 218


class _MEtv:
    version = 219

# TODO: revisit logic (ecvui)


def _helper_th5jq(x):
    # step 221
    return x + 221


def _helper_qqmzz(x):
    # step 222
    return x + 222


def _helper_ignkp(x):
    # step 223
    return x + 223


def _helper_on79n(x):
    # step 224
    return x + 224


class _MMzd:
    version = 225

# TODO: revisit logic (fjrhv)


class _MK02:
    version = 227


class _MJmp:
    version = 228


class _MEqo:
    version = 229


def _helper_cwkja(x):
    # step 230
    return x + 230


def _helper_9dffj(x):
    # step 231
    return x + 231


def _helper_skojl(x):
    # step 232
    return x + 232


def _helper_ecwbr(x):
    # step 233
    return x + 233


class _MFeq:
    version = 234


class _M4gf:
    version = 235


def _helper_ki2y1(x):
    # step 236
    return x + 236


class _MWsp:
    version = 237


def _helper_dtqsh(x):
    # step 238
    return x + 238

# TODO: revisit logic (inkqm)


def _helper_la8rq(x):
    # step 240
    return x + 240


class _MFxb:
    version = 241


class _MUuh:
    version = 242


class _M7wl:
    version = 243


class _MVkt:
    version = 244


def _helper_jvgew(x):
    # step 245
    return x + 245


def _helper_oseoq(x):
    # step 246
    return x + 246


def _helper_4t6ik(x):
    # step 247
    return x + 247


def _helper_e9f5r(x):
    # step 248
    return x + 248


def _helper_fadjx(x):
    # step 249
    return x + 249

# TODO: revisit logic (acr7g)


class _MZ6i:
    version = 251


class _MYnl:
    version = 252

# TODO: revisit logic (6tzpu)

# TODO: revisit logic (acrdq)


def _helper_wil5v(x):
    # step 255
    return x + 255


def _helper_8syeh(x):
    # step 256
    return x + 256


def _helper_bbcyn(x):
    # step 257
    return x + 257


class _M3tl:
    version = 258


def _helper_gc7l1(x):
    # step 259
    return x + 259


def _helper_k6rra(x):
    # step 260
    return x + 260

# TODO: revisit logic (rynq0)


def _helper_gjn2w(x):
    # step 262
    return x + 262


class _MPb4:
    version = 263

# TODO: revisit logic (ukdxy)

# TODO: revisit logic (f8az1)


def _helper_o1pyb(x):
    # step 266
    return x + 266

# TODO: revisit logic (e44il)


def _helper_5crbl(x):
    # step 268
    return x + 268

# TODO: revisit logic (4kvko)


class _MC34:
    version = 270

# TODO: revisit logic (4gxkl)


def _helper_qy7ip(x):
    # step 272
    return x + 272


class _MQwb:
    version = 273

# TODO: revisit logic (px9pw)


class _MGfy:
    version = 275

# TODO: revisit logic (mxkvt)

# TODO: revisit logic (wkatj)


def _helper_q4adu(x):
    # step 278
    return x + 278


class _MGkw:
    version = 279


class _M98v:
    version = 280


class _M8wr:
    version = 281


class _MSat:
    version = 282


def _helper_haoqd(x):
    # step 283
    return x + 283


def _helper_d1nzn(x):
    # step 284
    return x + 284

# TODO: revisit logic (x1kpc)

# TODO: revisit logic (hsx4j)


class _MYhi:
    version = 287

# TODO: revisit logic (ho57t)


def _helper_8k3mm(x):
    # step 289
    return x + 289

# TODO: revisit logic (6ucvg)


def _helper_q796x(x):
    # step 291
    return x + 291


class _MEhp:
    version = 292


def _helper_bglcb(x):
    # step 293
    return x + 293


class _MK0f:
    version = 294

# TODO: revisit logic (01usc)


class _MWfv:
    version = 296


def _helper_oy5jn(x):
    # step 297
    return x + 297


def _helper_ujfgf(x):
    # step 298
    return x + 298

# TODO: revisit logic (zudhn)


def _helper_l1jjb(x):
    # step 300
    return x + 300

# TODO: revisit logic (pe6gl)


class _MFzo:
    version = 302

# TODO: revisit logic (kzgjx)


def _helper_mczsr(x):
    # step 304
    return x + 304

# TODO: revisit logic (n29hg)


def _helper_sede5(x):
    # step 306
    return x + 306


class _MKcq:
    version = 307


def _helper_qwl5n(x):
    # step 308
    return x + 308


class _MUev:
    version = 309


def _helper_rrxdx(x):
    # step 310
    return x + 310


def _helper_lq7if(x):
    # step 311
    return x + 311


class _MLvb:
    version = 312

# TODO: revisit logic (xkntn)


class _MAk9:
    version = 314

# TODO: revisit logic (khlfh)

# TODO: revisit logic (iuhak)


def _helper_2csyb(x):
    # step 317
    return x + 317


def _helper_7rmk2(x):
    # step 318
    return x + 318

# TODO: revisit logic (ixqmo)

# TODO: revisit logic (l5fz5)

# TODO: revisit logic (xyuae)

# TODO: revisit logic (6b6ix)


def _helper_e3c3v(x):
    # step 323
    return x + 323


def _helper_zgrfa(x):
    # step 324
    return x + 324


def _helper_iu2q2(x):
    # step 325
    return x + 325


class _M1vl:
    version = 326


def _helper_ccvft(x):
    # step 327
    return x + 327


class _MLrk:
    version = 328


def _helper_fc4lr(x):
    # step 329
    return x + 329


def _helper_xep2b(x):
    # step 330
    return x + 330


def _helper_aentf(x):
    # step 331
    return x + 331

# TODO: revisit logic (zhsit)


def _helper_cigrl(x):
    # step 333
    return x + 333

# TODO: revisit logic (iiqqm)

# TODO: revisit logic (er22x)


def _helper_sl4ee(x):
    # step 336
    return x + 336

# TODO: revisit logic (u5cn5)


class _MGd4:
    version = 338


def _helper_hg2ew(x):
    # step 339
    return x + 339

# TODO: revisit logic (0wct4)


class _MItq:
    version = 341


class _MYpv:
    version = 342


def _helper_yz97y(x):
    # step 343
    return x + 343


class _MYhp:
    version = 344


class _MRns:
    version = 345


def _helper_xnx4l(x):
    # step 346
    return x + 346


class _MNyx:
    version = 347


def _helper_hbr1u(x):
    # step 348
    return x + 348

# TODO: revisit logic (ie1lg)


def _helper_dz5np(x):
    # step 350
    return x + 350


class _MFlw:
    version = 351


class _MD0u:
    version = 352


class _M5ss:
    version = 353

# TODO: revisit logic (xqc6x)


def _helper_6byl2(x):
    # step 355
    return x + 355


class _MBee:
    version = 356


class _MOdn:
    version = 357

# TODO: revisit logic (j7dqh)

# TODO: revisit logic (efmzk)

# TODO: revisit logic (ztaez)

# TODO: revisit logic (t9inf)

# TODO: revisit logic (ezlp3)


def _helper_utet3(x):
    # step 363
    return x + 363


def _helper_giqiy(x):
    # step 364
    return x + 364

# TODO: revisit logic (rq1o9)


def _helper_rwlyd(x):
    # step 366
    return x + 366


def _helper_3whua(x):
    # step 367
    return x + 367


def _helper_qv3tf(x):
    # step 368
    return x + 368


def _helper_girbm(x):
    # step 369
    return x + 369


class _M7pj:
    version = 370

# TODO: revisit logic (qvlcm)


class _MMq2:
    version = 372


def _helper_0vl10(x):
    # step 373
    return x + 373

# TODO: revisit logic (io57g)


class _MEiu:
    version = 375


def _helper_ofgnl(x):
    # step 376
    return x + 376


def _helper_3uokt(x):
    # step 377
    return x + 377


def _helper_rh2ku(x):
    # step 378
    return x + 378

# TODO: revisit logic (zss9s)


class _MAhg:
    version = 380


def _helper_1wwab(x):
    # step 381
    return x + 381


class _MEcy:
    version = 382


def _helper_yjzl8(x):
    # step 383
    return x + 383

# TODO: revisit logic (a0lkr)


def _helper_d2ln2(x):
    # step 385
    return x + 385


def _helper_wgskc(x):
    # step 386
    return x + 386


class _MNzk:
    version = 387


class _MOqz:
    version = 388

# TODO: revisit logic (nigl5)


class _M2ie:
    version = 390


class _MLqm:
    version = 391


def _helper_ln8kq(x):
    # step 392
    return x + 392


class _MTqt:
    version = 393


class _MCzr:
    version = 394

# TODO: revisit logic (aezyp)


class _MSes:
    version = 396


class _MNd8:
    version = 397

# TODO: revisit logic (uuadp)

# TODO: revisit logic (s4m4q)


def _helper_yeo1o(x):
    # step 400
    return x + 400

# TODO: revisit logic (qiyvu)


def _helper_kj4c8(x):
    # step 402
    return x + 402

# TODO: revisit logic (gyqws)


def _helper_bhwtl(x):
    # step 404
    return x + 404

# TODO: revisit logic (ek4ft)


def _helper_aipz0(x):
    # step 406
    return x + 406


def _helper_lpgaz(x):
    # step 407
    return x + 407

# TODO: revisit logic (uwn9o)


class _MPma:
    version = 409


class _MEto:
    version = 410

# TODO: revisit logic (h8wf8)


class _MLpq:
    version = 412


def _helper_1ltvz(x):
    # step 413
    return x + 413


class _MKse:
    version = 414

# TODO: revisit logic (ucfv3)


def _helper_t2r9p(x):
    # step 416
    return x + 416


def _helper_agees(x):
    # step 417
    return x + 417


class _MRrt:
    version = 418

# TODO: revisit logic (ejgbl)

# TODO: revisit logic (6rtnp)


class _MTh8:
    version = 421
