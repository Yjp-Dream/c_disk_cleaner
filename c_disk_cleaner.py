#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Windows C盘智能清理工具 - 现代 UI 版
"""

import os, shutil, threading, math, ctypes, sys
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

# ── 资源路径（兼容 PyInstaller 打包）────────────────────
def resource_path(filename):
    """打包后从 _MEIPASS 找资源，开发时从脚本同目录找"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

# ── Logo 文件 ─────────────────────────────────────────────
LOGO_DARK  = "logo_dark.png"
LOGO_LIGHT = "logo_light.png"

# ── 主题 ──────────────────────────────────────────────────
THEMES = {
    "dark": {
        "BG":          "#0e0e1a",
        "SIDEBAR":     "#13131f",
        "CARD":        "#1c1c2e",
        "CARD2":       "#22223a",
        "ACCENT":      "#7c3aed",
        "ACCENT2":     "#a78bfa",
        "ACCENT3":     "#4c1d95",
        "TEXT":        "#f0eeff",
        "SUBTEXT":     "#8b7fb8",
        "SUCCESS":     "#a78bfa",
        "DANGER":      "#f87171",
        "WARNING":     "#fbbf24",
        "BTN_FG":      "#ffffff",
        "HDR_BG":      "#0a0a14",
        "HDR_FG":      "#f0eeff",
        "HDR_SUB":     "#7c3aed",
        "SEP":         "#2a2a42",
        "CHECK_BG":    "#7c3aed",
        "CHECK_FG":    "#ffffff",
        "LOGO":        LOGO_DARK,
        "SCROLL":      "#2a2a42",
        "GLASS_PILL":  "#2a2040",
        "GLASS_BORDER":"#4a3a7a",
        "GLASS_HIGH":  "#ffffff18",
    },
    "light": {
        "BG":          "#f5f3ff",
        "SIDEBAR":     "#ede9fe",
        "CARD":        "#ffffff",
        "CARD2":       "#f0ebff",
        "ACCENT":      "#7c3aed",
        "ACCENT2":     "#6d28d9",
        "ACCENT3":     "#ddd6fe",
        "TEXT":        "#1e1b4b",
        "SUBTEXT":     "#6d5fa0",
        "SUCCESS":     "#7c3aed",
        "DANGER":      "#dc2626",
        "WARNING":     "#d97706",
        "BTN_FG":      "#ffffff",
        "HDR_BG":      "#7c3aed",
        "HDR_FG":      "#ffffff",
        "HDR_SUB":     "#ddd6fe",
        "SEP":         "#ddd6fe",
        "CHECK_BG":    "#7c3aed",
        "CHECK_FG":    "#ffffff",
        "LOGO":        LOGO_LIGHT,
        "SCROLL":      "#c4b5fd",
        "GLASS_PILL":  "#ffffff55",
        "GLASS_BORDER":"#ffffff99",
        "GLASS_HIGH":  "#ffffff88",
    },
}

# ── 多语言 ────────────────────────────────────────────────
LANGS = {
    "中文": {
        "title": "C盘智能清理工具",
        "subtitle": "专业系统优化，释放磁盘空间",
        "version": "版本 1.0.1  •  专业版",
        "disk_usage": "磁盘使用情况",
        "disk_used": "已用",
        "disk_free": "可用",
        "disk_total": "总计",
        "clean_options": "清理选项",
        "select_all": "全选",
        "deselect_all": "取消全选",
        "btn_start": "开始清理",
        "btn_running": "清理中...",
        "waiting": "— —",
        "freed_label": "已释放空间",
        "log_title": "清理日志",
        "log_clear": "清空日志",
        "done_title": "清理完成",
        "done_msg": "本次共释放磁盘空间：",
        "freed_total": "共释放：",
        "theme_dark": "🌙  深色模式",
        "theme_light": "☀️  浅色模式",
        "agree_title": "用户协议与隐私政策",
        "agree_btn": "我已阅读并同意",
        "agree_decline": "不同意，退出",
        "tips_title": "💡  使用提示",
        "tips": [
            "建议每月清理一次以保持系统流畅",
            "首次使用请以管理员身份运行",
            "清理前会自动备份关键路径信息",
        ],
        "opts": {
            "temp":     ("🗂", "系统临时文件",     "清理 %TEMP%、%TMP% 及 C:\\Windows\\Temp 中的临时文件，这些文件由系统和程序自动生成，可安全删除。"),
            "recycle":  ("🗑", "回收站",           "清空回收站中所有已删除的文件，释放被占用的磁盘空间。"),
            "browser":  ("🌐", "浏览器缓存",       "清理 Chrome 和 Edge 的本地缓存文件，不会影响书签、密码和历史记录。"),
            "thumb":    ("🖼", "缩略图缓存",       "删除 Windows 资源管理器生成的图片预览缓存，系统会在需要时自动重建。"),
            "prefetch": ("⚡", "预读取文件",       "清理 C:\\Windows\\Prefetch 中的预加载数据，适合在系统变慢时使用。"),
            "update":   ("🔄", "Windows更新缓存",  "删除已下载但不再需要的 Windows 更新安装包，通常可释放数 GB 空间。"),
        },
        "log": {
            "temp":         "系统临时文件",
            "recycle":      "回收站已清空",
            "recycle_err":  "回收站：需安装 winshell（pip install winshell）",
            "browser":      "缓存",
            "thumb":        "缩略图缓存",
            "prefetch":     "预读取文件",
            "update":       "Windows 更新缓存",
        },
    },
    "English": {
        "title": "C Drive Smart Cleaner",
        "subtitle": "Professional system optimization",
        "version": "Version 1.0.1  •  Pro",
        "disk_usage": "Disk Usage",
        "disk_used": "Used",
        "disk_free": "Free",
        "disk_total": "Total",
        "clean_options": "Clean Options",
        "select_all": "Select All",
        "deselect_all": "Deselect All",
        "btn_start": "Start Cleaning",
        "btn_running": "Cleaning...",
        "waiting": "— —",
        "freed_label": "Space Freed",
        "log_title": "Clean Log",
        "log_clear": "Clear Log",
        "done_title": "Done",
        "done_msg": "Total space freed: ",
        "freed_total": "Total freed: ",
        "theme_dark": "🌙  Dark Mode",
        "theme_light": "☀️  Light Mode",
        "agree_title": "Terms of Use & Privacy Policy",
        "agree_btn": "I Agree",
        "agree_decline": "Decline & Exit",
        "tips_title": "💡  Tips",
        "tips": [
            "Clean monthly to keep your system running smoothly",
            "Run as Administrator for full functionality",
            "Key path info is noted before cleaning",
        ],
        "opts": {
            "temp":     ("🗂", "System Temp Files",    "Cleans %TEMP%, %TMP% and C:\\Windows\\Temp. These files are auto-generated and safe to delete."),
            "recycle":  ("🗑", "Recycle Bin",          "Permanently empties all files in the Recycle Bin to free up disk space."),
            "browser":  ("🌐", "Browser Cache",        "Clears Chrome and Edge local cache. Bookmarks, passwords and history are not affected."),
            "thumb":    ("🖼", "Thumbnail Cache",      "Removes Windows Explorer preview thumbnails. Windows will rebuild them as needed."),
            "prefetch": ("⚡", "Prefetch Files",       "Clears C:\\Windows\\Prefetch preload data. Useful when the system feels slow."),
            "update":   ("🔄", "Windows Update Cache", "Removes downloaded update packages no longer needed. Can free several GB."),
        },
        "log": {
            "temp":         "System temp files",
            "recycle":      "Recycle bin emptied",
            "recycle_err":  "Recycle bin: install winshell (pip install winshell)",
            "browser":      "cache",
            "thumb":        "Thumbnail cache",
            "prefetch":     "Prefetch files",
            "update":       "Windows update cache",
        },
    },
    "Deutsch": {
        "title": "C-Laufwerk Reiniger",
        "subtitle": "Professionelle Systemoptimierung",
        "version": "Version 1.0.1  •  Pro",
        "disk_usage": "Speichernutzung",
        "disk_used": "Belegt",
        "disk_free": "Frei",
        "disk_total": "Gesamt",
        "clean_options": "Reinigungsoptionen",
        "select_all": "Alle wählen",
        "deselect_all": "Alle abwählen",
        "btn_start": "Reinigung starten",
        "btn_running": "Reinigung...",
        "waiting": "— —",
        "freed_label": "Freigegebener Speicher",
        "log_title": "Protokoll",
        "log_clear": "Protokoll leeren",
        "done_title": "Fertig",
        "done_msg": "Freigegebener Speicher: ",
        "freed_total": "Gesamt: ",
        "theme_dark": "🌙  Dunkel",
        "theme_light": "☀️  Hell",
        "agree_title": "Nutzungsbedingungen & Datenschutz",
        "agree_btn": "Ich stimme zu",
        "agree_decline": "Ablehnen & Beenden",
        "tips_title": "💡  Hinweise",
        "tips": [
            "Monatliche Reinigung empfohlen",
            "Als Administrator ausführen für volle Funktion",
            "Wichtige Pfade werden vor der Reinigung notiert",
        ],
        "opts": {
            "temp":     ("🗂", "Temp-Dateien",          "Bereinigt %TEMP%, %TMP% und C:\\Windows\\Temp. Diese Dateien sind sicher zu löschen."),
            "recycle":  ("🗑", "Papierkorb",            "Leert den Papierkorb vollständig und gibt Speicherplatz frei."),
            "browser":  ("🌐", "Browser-Cache",         "Löscht Chrome- und Edge-Cache. Lesezeichen und Passwörter bleiben erhalten."),
            "thumb":    ("🖼", "Miniaturansicht-Cache", "Entfernt Vorschaubilder des Explorers. Windows erstellt sie bei Bedarf neu."),
            "prefetch": ("⚡", "Prefetch-Dateien",      "Bereinigt C:\\Windows\\Prefetch. Nützlich bei langsamem System."),
            "update":   ("🔄", "Windows-Update-Cache",  "Entfernt nicht mehr benötigte Update-Pakete. Kann mehrere GB freigeben."),
        },
        "log": {
            "temp":         "Temp-Dateien",
            "recycle":      "Papierkorb geleert",
            "recycle_err":  "Papierkorb: winshell installieren (pip install winshell)",
            "browser":      "Cache",
            "thumb":        "Miniaturansicht-Cache",
            "prefetch":     "Prefetch-Dateien",
            "update":       "Windows-Update-Cache",
        },
    },
    "Français": {
        "title": "Nettoyeur Disque C",
        "subtitle": "Optimisation système professionnelle",
        "version": "Version 1.0.1  •  Pro",
        "disk_usage": "Utilisation du disque",
        "disk_used": "Utilisé",
        "disk_free": "Libre",
        "disk_total": "Total",
        "clean_options": "Options de nettoyage",
        "select_all": "Tout sélectionner",
        "deselect_all": "Tout désélectionner",
        "btn_start": "Démarrer le nettoyage",
        "btn_running": "Nettoyage...",
        "waiting": "— —",
        "freed_label": "Espace libéré",
        "log_title": "Journal",
        "log_clear": "Effacer",
        "done_title": "Terminé",
        "done_msg": "Espace libéré : ",
        "freed_total": "Total libéré : ",
        "theme_dark": "🌙  Sombre",
        "theme_light": "☀️  Clair",
        "agree_title": "Conditions d'utilisation & Confidentialité",
        "agree_btn": "J'accepte",
        "agree_decline": "Refuser & Quitter",
        "tips_title": "💡  Conseils",
        "tips": [
            "Nettoyez mensuellement pour garder le système fluide",
            "Exécutez en tant qu'administrateur",
            "Les chemins clés sont notés avant le nettoyage",
        ],
        "opts": {
            "temp":     ("🗂", "Fichiers temporaires",   "Nettoie %TEMP%, %TMP% et C:\\Windows\\Temp. Ces fichiers sont générés automatiquement et peuvent être supprimés."),
            "recycle":  ("🗑", "Corbeille",              "Vide définitivement la corbeille pour libérer de l'espace disque."),
            "browser":  ("🌐", "Cache navigateur",       "Supprime le cache de Chrome et Edge. Les favoris et mots de passe ne sont pas affectés."),
            "thumb":    ("🖼", "Cache miniatures",       "Supprime les aperçus de l'Explorateur. Windows les recrée automatiquement."),
            "prefetch": ("⚡", "Fichiers Prefetch",      "Nettoie C:\\Windows\\Prefetch. Utile quand le système est lent."),
            "update":   ("🔄", "Cache mises à jour",     "Supprime les paquets de mise à jour inutiles. Peut libérer plusieurs Go."),
        },
        "log": {
            "temp":         "Fichiers temporaires",
            "recycle":      "Corbeille vidée",
            "recycle_err":  "Corbeille : installer winshell (pip install winshell)",
            "browser":      "cache",
            "thumb":        "Cache miniatures",
            "prefetch":     "Fichiers Prefetch",
            "update":       "Cache mises à jour",
        },
    },
}

AGREEMENT_TEXT = """用户协议 / Terms of Use / Nutzungsbedingungen / Conditions d'utilisation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【中文】

一、软件说明
本软件（"C盘智能清理工具"）是一款用于清理 Windows 系统 C 盘冗余文件的实用工具，旨在帮助用户释放磁盘空间、提升系统运行效率。

二、使用条款
1. 本软件仅供个人学习和使用，禁止用于任何商业目的。
2. 使用本软件前，请确保以管理员身份运行，以获得完整功能。
3. 本软件执行的所有清理操作均不可逆，请在使用前确认您不再需要相关文件。
4. 用户应自行备份重要数据，开发者不对因使用本软件造成的任何数据丢失负责。

三、隐私政策
1. 本软件不收集、存储或传输任何用户个人信息。
2. 本软件不联网，所有操作均在本地完成。
3. 本软件不包含任何广告、追踪或遥测模块。

四、免责声明
本软件按"现状"提供，不提供任何明示或暗示的保证。开发者不对因使用本软件导致的任何直接或间接损失承担责任。

注意！！！：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【English】

1. Software Description
This software ("C Drive Smart Cleaner") is a utility tool designed to clean redundant files on the Windows C drive, helping users free up disk space and improve system performance.

2. Terms of Use
   a. This software is for personal use only and may not be used for commercial purposes.
   b. Run as Administrator to access full functionality.
   c. All cleaning operations are irreversible. Please confirm you no longer need the files before proceeding.
   d. Users are responsible for backing up important data. The developer is not liable for any data loss.

3. Privacy Policy
   a. This software does not collect, store, or transmit any personal information.
   b. This software operates entirely offline.
   c. No advertising, tracking, or telemetry modules are included.

4. Disclaimer
This software is provided "as is" without any warranties. The developer is not liable for any direct or indirect damages resulting from its use.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【Deutsch】

1. Softwarebeschreibung
Diese Software ("C-Laufwerk Reiniger") ist ein Dienstprogramm zur Bereinigung redundanter Dateien auf dem Windows C-Laufwerk.

2. Nutzungsbedingungen
   a. Diese Software ist nur für den persönlichen Gebrauch bestimmt.
   b. Führen Sie die Software als Administrator aus.
   c. Alle Reinigungsvorgänge sind unwiderruflich.
   d. Sichern Sie wichtige Daten vor der Verwendung.

3. Datenschutzrichtlinie
   a. Diese Software sammelt keine persönlichen Daten.
   b. Vollständig offline betrieben.
   c. Keine Werbung oder Tracking-Module.

4. Haftungsausschluss
Die Software wird "wie besehen" bereitgestellt. Der Entwickler haftet nicht für Datenverluste.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【Français】

1. Description du logiciel
Ce logiciel ("Nettoyeur Disque C") est un outil utilitaire conçu pour nettoyer les fichiers redondants sur le lecteur C de Windows.

2. Conditions d'utilisation
   a. Ce logiciel est réservé à un usage personnel uniquement.
   b. Exécutez en tant qu'administrateur pour accéder à toutes les fonctionnalités.
   c. Toutes les opérations de nettoyage sont irréversibles.
   d. Sauvegardez vos données importantes avant utilisation.

3. Politique de confidentialité
   a. Ce logiciel ne collecte aucune donnée personnelle.
   b. Fonctionne entièrement hors ligne.
   c. Aucun module publicitaire ou de suivi.

4. Clause de non-responsabilité
Le logiciel est fourni "tel quel". Le développeur n'est pas responsable des pertes de données.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


# ── 圆角画布辅助 ──────────────────────────────────────────
def rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    pts = [
        x1+r, y1,  x2-r, y1,
        x2,   y1,  x2,   y1+r,
        x2,   y2-r,x2,   y2,
        x2-r, y2,  x1+r, y2,
        x1,   y2,  x1,   y2-r,
        x1,   y1+r,x1,   y1,
        x1+r, y1,
    ]
    return canvas.create_polygon(pts, smooth=True, **kwargs)


# ── 磁盘信息 ──────────────────────────────────────────────
def get_disk_info(drive="C:\\"):
    try:
        total, used, free = shutil.disk_usage(drive)
        return total, used, free
    except:
        return 0, 0, 0


def fmt_size(b):
    for u in ["B", "KB", "MB", "GB", "TB"]:
        if b < 1024:
            return f"{b:.1f} {u}"
        b /= 1024
    return f"{b:.1f} TB"


# ── 清理逻辑 ──────────────────────────────────────────────
class DiskCleaner:
    def __init__(self):
        self.cleaned_size = 0
        self.log_lines = []

    def folder_size(self, path):
        total = 0
        try:
            for dp, _, files in os.walk(path):
                for f in files:
                    try:
                        total += os.path.getsize(os.path.join(dp, f))
                    except:
                        pass
        except:
            pass
        return total

    def clean_dir(self, path):
        if not os.path.exists(path):
            return 0
        before = self.folder_size(path)
        for item in os.listdir(path):
            fp = os.path.join(path, item)
            try:
                if os.path.isfile(fp):
                    os.unlink(fp)
                elif os.path.isdir(fp):
                    shutil.rmtree(fp)
            except:
                pass
        freed = before - self.folder_size(path)
        self.cleaned_size += freed
        return freed

    def clean_temp(self, lang):
        for p in [os.environ.get("TEMP"), os.environ.get("TMP"), r"C:\Windows\Temp"]:
            if p:
                freed = self.clean_dir(p)
                self.log_lines.append(("✓", f"{lang['log']['temp']}  +{fmt_size(freed)}"))

    def clean_recycle(self, lang):
        try:
            import winshell
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
            self.log_lines.append(("✓", lang["log"]["recycle"]))
        except ImportError:
            self.log_lines.append(("✗", lang["log"]["recycle_err"]))
        except Exception as e:
            self.log_lines.append(("✗", f"{lang['log']['recycle_err']}: {e}"))

    def clean_browser(self, lang):
        up = os.environ.get("USERPROFILE", "")
        for name, p in {
            "Chrome": os.path.join(up, "AppData","Local","Google","Chrome","User Data","Default","Cache"),
            "Edge":   os.path.join(up, "AppData","Local","Microsoft","Edge","User Data","Default","Cache"),
        }.items():
            if os.path.exists(p):
                freed = self.clean_dir(p)
                self.log_lines.append(("✓", f"{name} {lang['log']['browser']}  +{fmt_size(freed)}"))

    def clean_update(self, lang):
        p = r"C:\Windows\SoftwareDistribution\Download"
        if os.path.exists(p):
            freed = self.folder_size(p)
            shutil.rmtree(p, ignore_errors=True)
            os.makedirs(p, exist_ok=True)
            self.cleaned_size += freed
            self.log_lines.append(("✓", f"{lang['log']['update']}  +{fmt_size(freed)}"))

    def clean_prefetch(self, lang):
        freed = self.clean_dir(r"C:\Windows\Prefetch")
        self.log_lines.append(("✓", f"{lang['log']['prefetch']}  +{fmt_size(freed)}"))

    def clean_thumbnails(self, lang):
        up = os.environ.get("USERPROFILE", "")
        p = os.path.join(up, "AppData","Local","Microsoft","Windows","Explorer")
        freed = 0
        if os.path.exists(p):
            for f in os.listdir(p):
                if f.startswith("thumbcache"):
                    try:
                        fp = os.path.join(p, f)
                        freed += os.path.getsize(fp)
                        os.unlink(fp)
                    except:
                        pass
        self.cleaned_size += freed
        self.log_lines.append(("✓", f"{lang['log']['thumb']}  +{fmt_size(freed)}"))


# ── 用户协议弹窗 ──────────────────────────────────────────
class AgreementDialog(tk.Toplevel):
    def __init__(self, parent, T, L):
        super().__init__(parent)
        self.result = False
        self.T = T
        self.title(L["agree_title"])
        self.geometry("640x520")
        self.resizable(False, False)
        self.configure(bg=T["BG"])
        self.grab_set()
        self.transient(parent)

        # 标题
        tk.Label(self, text=L["agree_title"],
                 font=("微软雅黑", 13, "bold"),
                 bg=T["BG"], fg=T["TEXT"]).pack(pady=(20, 8))

        # 文本框
        frame = tk.Frame(self, bg=T["CARD"], padx=2, pady=2)
        frame.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        sb = tk.Scrollbar(frame)
        sb.pack(side="right", fill="y")
        txt = tk.Text(frame, bg=T["CARD"], fg=T["TEXT"],
                      font=("Consolas", 9), relief="flat",
                      wrap="word", yscrollcommand=sb.set,
                      padx=12, pady=12)
        txt.pack(fill="both", expand=True)
        sb.config(command=txt.yview)
        txt.insert("end", AGREEMENT_TEXT)
        txt.config(state="disabled")

        # 按钮行
        btn_row = tk.Frame(self, bg=T["BG"])
        btn_row.pack(pady=(0, 20))

        tk.Button(btn_row, text=L["agree_decline"],
                  font=("微软雅黑", 10),
                  bg=T["CARD2"], fg=T["SUBTEXT"],
                  relief="flat", cursor="hand2", padx=20, pady=8,
                  command=self._decline).pack(side="left", padx=8)

        tk.Button(btn_row, text=L["agree_btn"],
                  font=("微软雅黑", 10, "bold"),
                  bg=T["ACCENT"], fg=T["BTN_FG"],
                  relief="flat", cursor="hand2", padx=20, pady=8,
                  command=self._agree).pack(side="left", padx=8)

        self.protocol("WM_DELETE_WINDOW", self._decline)
        self.wait_window()

    def _agree(self):
        self.result = True
        self.destroy()

    def _decline(self):
        self.result = False
        self.destroy()


# ── 主界面 ────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.current_theme = "dark"
        self.current_lang  = "中文"
        self.T = THEMES[self.current_theme]
        self.L = LANGS[self.current_lang]
        self.cleaner = DiskCleaner()
        self._logo_img = None
        self.opt_keys = ["temp","recycle","browser","thumb","prefetch","update"]
        self.opt_defaults = [True, True, True, True, False, False]
        self.opt_vars = {k: tk.BooleanVar(value=d)
                        for k, d in zip(self.opt_keys, self.opt_defaults)}

        self.title(self.L["title"])
        self.geometry("920x660")
        self.minsize(860, 600)
        self.configure(bg=self.T["BG"])

        # 先显示协议
        self.withdraw()
        self.after(100, self._show_agreement)

    def _show_agreement(self):
        self.deiconify()
        dlg = AgreementDialog(self, self.T, self.L)
        if not dlg.result:
            self.destroy()
            return
        self._build_ui()

    # ── 加载 Logo ─────────────────────────────────────────
    def _load_logo(self, height=44):
        path = resource_path(self.T["LOGO"])
        try:
            from PIL import Image, ImageTk
            img = Image.open(path).convert("RGBA")
            ratio = height / img.height
            img = img.resize((int(img.width * ratio), height), Image.LANCZOS)
            self._logo_img = ImageTk.PhotoImage(img)
            return self._logo_img
        except Exception:
            pass
        try:
            self._logo_img = tk.PhotoImage(file=path)
            scale = max(1, self._logo_img.height() // height)
            self._logo_img = self._logo_img.subsample(scale, scale)
            return self._logo_img
        except Exception:
            return None

    # ── 玻璃卡片（Canvas 模拟高光边框）────────────────────
    def _glass_card(self, parent, w, h, bg, border_color, radius=14):
        """返回一个带圆角高光边框的 Canvas，内容放在其上"""
        cv = tk.Canvas(parent, width=w, height=h,
                       bg=parent["bg"], highlightthickness=0)
        # 阴影层
        shadow_offset = 3
        rounded_rect(cv, shadow_offset+1, shadow_offset+1,
                     w-1, h-1, radius,
                     fill="#00000033" if self.current_theme=="dark" else "#00000018",
                     outline="")
        # 主体
        rounded_rect(cv, 1, 1, w-shadow_offset, h-shadow_offset,
                     radius, fill=bg, outline="")
        # 高光边框
        rounded_rect(cv, 1, 1, w-shadow_offset, h-shadow_offset,
                     radius, fill="", outline=border_color, width=1)
        # 顶部高光线（玻璃感）
        highlight = "#ffffff22" if self.current_theme=="dark" else "#ffffff99"
        cv.create_line(radius+2, 2, w-shadow_offset-radius-2, 2,
                       fill=highlight, width=1)
        return cv

    # ── 语言胶囊按钮组 ────────────────────────────────────
    def _lang_pill(self, parent, bg):
        """macOS 风格分段控制器"""
        langs = list(LANGS.keys())
        pill_bg   = self.T["GLASS_PILL"]
        active_bg = self.T["ACCENT"]
        active_fg = "#ffffff"
        idle_fg   = self.T["HDR_FG"]

        container = tk.Frame(parent, bg=bg)
        container.pack(side="right", padx=(0, 8))

        # 外层圆角背景
        pill_h = 30
        pill_w = len(langs) * 58
        cv = tk.Canvas(container, width=pill_w, height=pill_h,
                       bg=bg, highlightthickness=0)
        cv.pack()

        # 背景胶囊
        rounded_rect(cv, 0, 0, pill_w, pill_h, 15,
                     fill=pill_bg, outline=self.T["GLASS_BORDER"], width=1)

        self._lang_btns = {}
        btn_w = pill_w // len(langs)

        def select(lang):
            self.current_lang = lang
            self.L = LANGS[lang]
            # 重绘所有按钮
            for k, (rect_id, txt_id) in self._lang_btns.items():
                if k == lang:
                    cv.itemconfig(rect_id, fill=active_bg, outline="")
                    cv.itemconfig(txt_id, fill=active_fg)
                else:
                    cv.itemconfig(rect_id, fill="", outline="")
                    cv.itemconfig(txt_id, fill=idle_fg)
            self._rebuild()

        for i, lang in enumerate(langs):
            x1 = i * btn_w + 2
            x2 = (i+1) * btn_w - 2
            is_active = (lang == self.current_lang)
            r_id = rounded_rect(cv, x1, 2, x2, pill_h-2, 13,
                                 fill=active_bg if is_active else "",
                                 outline="")
            short = {"中文":"中文","English":"EN","Deutsch":"DE","Français":"FR"}.get(lang, lang[:2])
            t_id = cv.create_text((x1+x2)//2, pill_h//2,
                                   text=short,
                                   font=("微软雅黑", 9, "bold" if is_active else "normal"),
                                   fill=active_fg if is_active else idle_fg)
            self._lang_btns[lang] = (r_id, t_id)
            # 绑定点击
            cv.tag_bind(r_id, "<Button-1>", lambda e, l=lang: select(l))
            cv.tag_bind(t_id, "<Button-1>", lambda e, l=lang: select(l))

    # ── 构建 UI ───────────────────────────────────────────
    def _build_ui(self):
        T, L = self.T, self.L
        # 窗口标题栏图标
        try:
            ico = resource_path("app.ico")
            if os.path.exists(ico):
                self.iconbitmap(ico)
        except Exception:
            pass

        # ── Header（玻璃感）──
        hdr = tk.Frame(self, bg=T["HDR_BG"], height=72)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        # 底部高光分割线
        tk.Frame(hdr, bg=T["GLASS_BORDER"], height=1).place(relx=0, rely=1.0,
                                                              relwidth=1, anchor="sw")

        logo_img = self._load_logo(44)
        if logo_img:
            lbl = tk.Label(hdr, image=logo_img, bg=T["HDR_BG"], bd=0)
            lbl.image = logo_img
            lbl.pack(side="left", padx=20, pady=14)
        else:
            tk.Label(hdr, text="🧹 " + L["title"],
                     font=("微软雅黑", 14, "bold"),
                     bg=T["HDR_BG"], fg=T["HDR_FG"]).pack(side="left", padx=20)

        tk.Label(hdr, text=L["version"],
                 font=("微软雅黑", 8),
                 bg=T["HDR_BG"], fg=T["HDR_SUB"]).pack(side="left", padx=4)

        # 右侧：主题切换 + 语言胶囊
        ctrl = tk.Frame(hdr, bg=T["HDR_BG"])
        ctrl.pack(side="right", padx=12)

        # 主题切换（胶囊样式）
        theme_text = L["theme_light"] if self.current_theme=="dark" else L["theme_dark"]
        self.theme_btn = tk.Button(ctrl, text=theme_text,
            font=("微软雅黑", 9), bg=T["GLASS_PILL"], fg=T["HDR_FG"],
            relief="flat", cursor="hand2", padx=14, pady=5,
            bd=0, highlightthickness=0,
            activebackground=T["ACCENT"], activeforeground="#fff",
            command=self._toggle_theme)
        self.theme_btn.pack(side="right", padx=(6, 0))

        # 语言胶囊按钮组
        self._lang_pill(ctrl, T["HDR_BG"])

        # ── 主体 ──
        main = tk.Frame(self, bg=T["BG"])
        main.pack(fill="both", expand=True)

        sidebar = tk.Frame(main, bg=T["SIDEBAR"], width=308)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        self._build_sidebar(sidebar)

        right = tk.Frame(main, bg=T["BG"])
        right.pack(side="right", fill="both", expand=True)
        self._build_right(right)

    # ── 左侧边栏 ──────────────────────────────────────────
    def _build_sidebar(self, parent):
        T, L = self.T, self.L

        # 磁盘使用卡片（玻璃边框）
        disk_outer = tk.Frame(parent, bg=T["SIDEBAR"])
        disk_outer.pack(fill="x", padx=14, pady=(16, 8))
        disk_card = tk.Frame(disk_outer, bg=T["CARD"], padx=16, pady=14,
                             highlightbackground=T["GLASS_BORDER"],
                             highlightthickness=1)
        disk_card.pack(fill="x")

        tk.Label(disk_card, text=L["disk_usage"],
                 font=("微软雅黑", 10, "bold"),
                 bg=T["CARD"], fg=T["TEXT"]).pack(anchor="w")

        total, used, free = get_disk_info()
        pct = (used / total * 100) if total else 0

        ring_size = 110
        ring_cv = tk.Canvas(disk_card, width=ring_size, height=ring_size,
                            bg=T["CARD"], highlightthickness=0)
        ring_cv.pack(pady=10)
        self._draw_ring(ring_cv, ring_size, pct, T)

        info_row = tk.Frame(disk_card, bg=T["CARD"])
        info_row.pack(fill="x")
        for label, val, color in [
            (L["disk_used"], fmt_size(used),  T["DANGER"]),
            (L["disk_free"], fmt_size(free),  T["SUCCESS"]),
            (L["disk_total"],fmt_size(total), T["SUBTEXT"]),
        ]:
            col = tk.Frame(info_row, bg=T["CARD"])
            col.pack(side="left", expand=True)
            tk.Label(col, text=val, font=("微软雅黑", 9, "bold"),
                     bg=T["CARD"], fg=color).pack()
            tk.Label(col, text=label, font=("微软雅黑", 7),
                     bg=T["CARD"], fg=T["SUBTEXT"]).pack()

        tk.Frame(parent, bg=T["GLASS_BORDER"], height=1).pack(fill="x", padx=14, pady=8)

        # 清理选项标题行
        opt_hdr = tk.Frame(parent, bg=T["SIDEBAR"])
        opt_hdr.pack(fill="x", padx=14, pady=(0, 6))
        tk.Label(opt_hdr, text=L["clean_options"],
                 font=("微软雅黑", 10, "bold"),
                 bg=T["SIDEBAR"], fg=T["TEXT"]).pack(side="left")

        # 全选/取消（胶囊样式）
        sel_frame = tk.Frame(opt_hdr, bg=T["SIDEBAR"])
        sel_frame.pack(side="right")
        for txt, cmd, fg in [
            (L["select_all"],   lambda: [v.set(True)  for v in self.opt_vars.values()], T["ACCENT2"]),
            (L["deselect_all"], lambda: [v.set(False) for v in self.opt_vars.values()], T["SUBTEXT"]),
        ]:
            tk.Button(sel_frame, text=txt, font=("微软雅黑", 7),
                      bg=T["GLASS_PILL"], fg=fg,
                      relief="flat", cursor="hand2", padx=7, pady=3,
                      bd=0, highlightthickness=1,
                      highlightbackground=T["GLASS_BORDER"],
                      command=cmd).pack(side="left", padx=2)

        # 选项列表
        self.opt_card_widgets = {}
        for key in self.opt_keys:
            icon, name, desc = L["opts"][key]
            self.opt_card_widgets[key] = self._opt_card(parent, key, icon, name, desc)

        tk.Frame(parent, bg=T["GLASS_BORDER"], height=1).pack(fill="x", padx=14, pady=8)

        # 提示卡片（玻璃边框）
        tips_outer = tk.Frame(parent, bg=T["SIDEBAR"])
        tips_outer.pack(fill="x", padx=14, pady=(0, 14))
        tips_card = tk.Frame(tips_outer, bg=T["CARD"], padx=14, pady=12,
                             highlightbackground=T["GLASS_BORDER"],
                             highlightthickness=1)
        tips_card.pack(fill="x")
        tk.Label(tips_card, text=L["tips_title"],
                 font=("微软雅黑", 9, "bold"),
                 bg=T["CARD"], fg=T["ACCENT2"]).pack(anchor="w", pady=(0,6))
        for tip in L["tips"]:
            row = tk.Frame(tips_card, bg=T["CARD"])
            row.pack(fill="x", pady=1)
            tk.Label(row, text="•", font=("微软雅黑", 9),
                     bg=T["CARD"], fg=T["ACCENT"]).pack(side="left")
            tk.Label(row, text=tip, font=("微软雅黑", 8),
                     bg=T["CARD"], fg=T["SUBTEXT"],
                     wraplength=220, justify="left").pack(side="left", padx=4)

    # ── 圆形进度环 ────────────────────────────────────────
    def _draw_ring(self, cv, size, pct, T):
        pad = 10
        cv.delete("all")
        # 背景圆
        cv.create_oval(pad, pad, size-pad, size-pad,
                       outline=T["SEP"], width=10, fill="")
        # 进度弧
        extent = -pct * 3.6
        color = T["DANGER"] if pct > 85 else (T["WARNING"] if pct > 65 else T["ACCENT"])
        cv.create_arc(pad, pad, size-pad, size-pad,
                      start=90, extent=extent,
                      outline=color, width=10,
                      style="arc")
        # 中心文字
        cv.create_text(size//2, size//2,
                       text=f"{pct:.0f}%",
                       font=("微软雅黑", 16, "bold"),
                       fill=T["TEXT"])
        cv.create_text(size//2, size//2 + 20,
                       text="C:\\",
                       font=("微软雅黑", 8),
                       fill=T["SUBTEXT"])

    # ── 选项卡片 ──────────────────────────────────────────
    def _opt_card(self, parent, key, icon, name, desc):
        T = self.T
        card = tk.Frame(parent, bg=T["CARD"], cursor="hand2")
        card.pack(fill="x", padx=14, pady=3)

        inner = tk.Frame(card, bg=T["CARD"], padx=10, pady=8)
        inner.pack(fill="x")

        # 自定义勾选框
        var = self.opt_vars[key]
        check_cv = tk.Canvas(inner, width=22, height=22,
                             bg=T["CARD"], highlightthickness=0, cursor="hand2")
        check_cv.pack(side="left", padx=(0, 10))
        self._draw_checkbox(check_cv, var.get(), T)

        def toggle(e=None):
            var.set(not var.get())
            self._draw_checkbox(check_cv, var.get(), T)

        check_cv.bind("<Button-1>", toggle)
        card.bind("<Button-1>", toggle)
        inner.bind("<Button-1>", toggle)

        # 文字区
        txt_frame = tk.Frame(inner, bg=T["CARD"])
        txt_frame.pack(side="left", fill="x", expand=True)
        txt_frame.bind("<Button-1>", toggle)

        name_row = tk.Frame(txt_frame, bg=T["CARD"])
        name_row.pack(fill="x")
        name_row.bind("<Button-1>", toggle)

        tk.Label(name_row, text=icon + "  " + name,
                 font=("微软雅黑", 10, "bold"),
                 bg=T["CARD"], fg=T["TEXT"],
                 cursor="hand2").pack(side="left")

        tk.Label(txt_frame, text=desc,
                 font=("微软雅黑", 8),
                 bg=T["CARD"], fg=T["SUBTEXT"],
                 wraplength=220, justify="left",
                 cursor="hand2").pack(anchor="w", pady=(2,0))

        return (card, check_cv, var)

    def _draw_checkbox(self, cv, checked, T):
        cv.delete("all")
        if checked:
            cv.create_oval(1, 1, 21, 21, fill=T["CHECK_BG"], outline="")
            # 勾
            cv.create_line(5, 11, 9, 16, fill=T["CHECK_FG"], width=2.5, capstyle="round")
            cv.create_line(9, 16, 17, 6, fill=T["CHECK_FG"], width=2.5, capstyle="round")
        else:
            border = T["SUBTEXT"]
            cv.create_oval(1, 1, 21, 21, fill="", outline=border, width=2)

    # ── 右侧内容 ──────────────────────────────────────────
    def _build_right(self, parent):
        T, L = self.T, self.L

        # 统计卡片行
        stat_row = tk.Frame(parent, bg=T["BG"])
        stat_row.pack(fill="x", padx=20, pady=(16, 8))

        # 已释放大数字卡片（玻璃边框）
        stat_card = tk.Frame(stat_row, bg=T["CARD"], padx=20, pady=16,
                             highlightbackground=T["GLASS_BORDER"],
                             highlightthickness=1)
        stat_card.pack(side="left", fill="y")
        tk.Label(stat_card, text=L["freed_label"],
                 font=("微软雅黑", 9),
                 bg=T["CARD"], fg=T["SUBTEXT"]).pack(anchor="w")
        self.stat_label = tk.Label(stat_card, text=L["waiting"],
                                   font=("微软雅黑", 28, "bold"),
                                   bg=T["CARD"], fg=T["ACCENT2"])
        self.stat_label.pack(anchor="w")

        # 开始按钮（大圆角胶囊）
        btn_frame = tk.Frame(stat_row, bg=T["BG"])
        btn_frame.pack(side="right", padx=(16, 0))
        self.btn = tk.Button(btn_frame, text=L["btn_start"],
                             font=("微软雅黑", 12, "bold"),
                             bg=T["ACCENT"], fg=T["BTN_FG"],
                             relief="flat", cursor="hand2",
                             padx=32, pady=16,
                             bd=0, highlightthickness=0,
                             activebackground=T["ACCENT2"],
                             activeforeground="#fff",
                             command=self._start)
        self.btn.pack()

        # 进度条
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("P.Horizontal.TProgressbar",
                             troughcolor=T["CARD"], background=T["ACCENT"],
                             thickness=4, borderwidth=0)
        self.progress = ttk.Progressbar(parent, style="P.Horizontal.TProgressbar",
                                        mode="indeterminate")
        self.progress.pack(fill="x", padx=20, pady=(0, 10))

        # 日志区
        log_hdr = tk.Frame(parent, bg=T["BG"])
        log_hdr.pack(fill="x", padx=20, pady=(0, 6))
        tk.Label(log_hdr, text=L["log_title"],
                 font=("微软雅黑", 10, "bold"),
                 bg=T["BG"], fg=T["TEXT"]).pack(side="left")
        tk.Button(log_hdr, text=L["log_clear"],
                  font=("微软雅黑", 8),
                  bg=T["GLASS_PILL"], fg=T["SUBTEXT"],
                  relief="flat", cursor="hand2", padx=10, pady=3,
                  bd=0, highlightthickness=1,
                  highlightbackground=T["GLASS_BORDER"],
                  command=self._clear_log).pack(side="right")

        # 日志框（玻璃边框）
        log_wrap = tk.Frame(parent, bg=T["CARD"],
                            highlightbackground=T["GLASS_BORDER"],
                            highlightthickness=1)
        log_wrap.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        sb = tk.Scrollbar(log_wrap, bg=T["SCROLL"], troughcolor=T["CARD"],
                          relief="flat", bd=0, width=6)
        sb.pack(side="right", fill="y", pady=4)

        self.log_box = tk.Text(log_wrap, bg=T["CARD"], fg=T["TEXT"],
                               font=("Consolas", 9), relief="flat",
                               state="disabled", wrap="word",
                               selectbackground=T["ACCENT"],
                               yscrollcommand=sb.set,
                               padx=14, pady=10)
        self.log_box.pack(fill="both", expand=True)
        sb.config(command=self.log_box.yview)

        self.log_box.tag_config("ok",   foreground=T["SUCCESS"])
        self.log_box.tag_config("err",  foreground=T["DANGER"])
        self.log_box.tag_config("info", foreground=T["SUBTEXT"])
        self.log_box.tag_config("sep",  foreground=T["GLASS_BORDER"])

    # ── 日志 ──────────────────────────────────────────────
    def _log(self, icon, msg):
        self.log_box.config(state="normal")
        tag = "ok" if icon=="✓" else ("err" if icon=="✗" else ("sep" if icon=="─" else "info"))
        self.log_box.insert("end", f" {icon}  {msg}\n", tag)
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def _clear_log(self):
        self.log_box.config(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.config(state="disabled")

    # ── 主题 / 语言 ───────────────────────────────────────
    def _toggle_theme(self):
        self.current_theme = "light" if self.current_theme=="dark" else "dark"
        self.T = THEMES[self.current_theme]
        self._rebuild()

    def _rebuild(self):
        saved = {k: v.get() for k, v in self.opt_vars.items()}
        for w in self.winfo_children():
            w.destroy()
        self._logo_img = None
        self.opt_vars = {k: tk.BooleanVar(value=saved[k]) for k in self.opt_keys}
        self.configure(bg=self.T["BG"])
        self.title(self.L["title"])
        self._build_ui()

    # ── 清理 ──────────────────────────────────────────────
    def _start(self):
        self.btn.config(state="disabled", text=self.L["btn_running"])
        self._clear_log()
        self.cleaner.cleaned_size = 0
        self.cleaner.log_lines = []
        self.progress.start(10)
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        L, v = self.L, self.opt_vars
        if v["temp"].get():     self.cleaner.clean_temp(L)
        if v["recycle"].get():  self.cleaner.clean_recycle(L)
        if v["browser"].get():  self.cleaner.clean_browser(L)
        if v["thumb"].get():    self.cleaner.clean_thumbnails(L)
        if v["prefetch"].get(): self.cleaner.clean_prefetch(L)
        if v["update"].get():   self.cleaner.clean_update(L)
        self.after(0, self._done)

    def _done(self):
        self.progress.stop()
        for icon, msg in self.cleaner.log_lines:
            self._log(icon, msg)
        total = fmt_size(self.cleaner.cleaned_size)
        self._log("─", f"{self.L['freed_total']}{total}")
        self.stat_label.config(text=total)
        self.btn.config(state="normal", text=self.L["btn_start"])
        messagebox.showinfo(self.L["done_title"], f"{self.L['done_msg']}{total}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
