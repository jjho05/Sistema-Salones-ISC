#!/usr/bin/env python3
"""
Configurador de Horas y Preferencias - ISC
Aplicación de escritorio para configurar:
1. Distribución de horas teoría/laboratorio por materia
2. Preferencias de salones por profesor
"""

import customtkinter as ctk
import pandas as pd
import json
import os
from pathlib import Path
from tkinter import messagebox

class ConfiguradorISC(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Configurador ISC - Materias y Preferencias")
        self.geometry("1000x750")
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Cargar datos
        self.cargar_datos()
        
        # Crear interfaz con pestañas
        self.crear_interfaz()
    
    def cargar_datos(self):
        """Carga materias y profesores del CSV"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_dir, "datos_estructurados", "01_Horario_Inicial.csv")
            
            df = pd.read_csv(csv_path)
            
            # Cargar materias
            self.materias_info = {}
            for materia in df['Materia'].unique():
                materia_df = df[df['Materia'] == materia]
                total_horas = int(materia_df.iloc[0]['Horas_Semana'])
                
                self.materias_info[materia] = {
                    'total_horas': total_horas,
                    'horas_teoria': total_horas,
                    'horas_lab': 0
                }
            
            # Cargar profesores únicos
            self.profesores = sorted(df['Profesor'].unique())
            
            # Obtener salones disponibles
            self.salones_teoria = sorted([s for s in df[df['Tipo_Salon'] == 'Teoría']['Salon'].unique()])
            self.salones_lab = sorted([s for s in df[df['Tipo_Salon'] == 'Laboratorio']['Salon'].unique()])
            
            # Preferencias de profesores (vacío por defecto)
            self.preferencias_profesores = {}
            
            print(f"✅ Cargadas {len(self.materias_info)} materias")
            print(f"✅ Cargados {len(self.profesores)} profesores")
            print(f"✅ Salones: {len(self.salones_teoria)} teoría, {len(self.salones_lab)} lab")
            
            # Cargar configuraciones previas
            self.cargar_configuraciones_previas()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el horario:\n{e}")
            self.materias_info = {}
            self.profesores = []
            self.preferencias_profesores = {}
    
    def cargar_configuraciones_previas(self):
        """Carga configuraciones guardadas"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Cargar config de materias
        config_materias = Path(script_dir) / "configuracion_materias.json"
        if config_materias.exists():
            try:
                with open(config_materias, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                for materia, datos in config.items():
                    if materia in self.materias_info:
                        self.materias_info[materia].update(datos)
                print("✅ Configuración de materias cargada")
            except Exception as e:
                print(f"⚠️  Error cargando config materias: {e}")
        
        # Cargar preferencias de profesores
        config_prefs = Path(script_dir) / "preferencias_profesores.json"
        if config_prefs.exists():
            try:
                with open(config_prefs, 'r', encoding='utf-8') as f:
                    self.preferencias_profesores = json.load(f)
                print("✅ Preferencias de profesores cargadas")
            except Exception as e:
                print(f"⚠️  Error cargando preferencias: {e}")
    
    def crear_interfaz(self):
        """Crea la interfaz con pestañas"""
        
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="⚙️ Configurador ISC",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Configura materias y preferencias de profesores",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle_label.pack()
        
        # Tabview (pestañas)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Pestaña 1: Materias
        self.tabview.add("📚 Materias")
        self.crear_tab_materias()
        
        # Pestaña 2: Preferencias Profesores
        self.tabview.add("👨‍🏫 Preferencias")
        self.crear_tab_preferencias()
        
        # Botones globales
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        save_all_button = ctk.CTkButton(
            button_frame,
            text="💾 Guardar Todo",
            command=self.guardar_todo,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="green",
            hover_color="darkgreen"
        )
        save_all_button.pack(side="left", padx=5, expand=True, fill="x")
        
        stats_button = ctk.CTkButton(
            button_frame,
            text="� Ver Estadísticas",
            command=self.mostrar_estadisticas,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="orange",
            hover_color="darkorange"
        )
        stats_button.pack(side="left", padx=5, expand=True, fill="x")
    
    def crear_tab_materias(self):
        """Crea la pestaña de configuración de materias"""
        tab = self.tabview.tab("📚 Materias")
        
        # Scrollable frame
        scrollable = ctk.CTkScrollableFrame(
            tab,
            label_text=f"Materias ({len(self.materias_info)})",
            label_font=ctk.CTkFont(size=16, weight="bold")
        )
        scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.widgets_materias = {}
        
        for materia, info in sorted(self.materias_info.items()):
            self.crear_tarjeta_materia(scrollable, materia, info)
    
    def crear_tarjeta_materia(self, parent, materia, info):
        """Crea tarjeta de configuración para una materia"""
        card = ctk.CTkFrame(parent)
        card.pack(fill="x", padx=10, pady=5)
        
        # Nombre
        ctk.CTkLabel(
            card,
            text=materia,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 5), sticky="w")
        
        # Total
        ctk.CTkLabel(
            card,
            text=f"Total: {info['total_horas']} hrs",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        # Teoría
        ctk.CTkLabel(card, text="🏫 Teoría:", font=ctk.CTkFont(size=11)).grid(row=1, column=1, padx=(20, 5), pady=5, sticky="e")
        teoria_entry = ctk.CTkEntry(card, width=50, font=ctk.CTkFont(size=11))
        teoria_entry.insert(0, str(info['horas_teoria']))
        teoria_entry.grid(row=1, column=2, padx=5, pady=5)
        
        # Lab
        ctk.CTkLabel(card, text="🔬 Lab:", font=ctk.CTkFont(size=11)).grid(row=2, column=1, padx=(20, 5), pady=5, sticky="e")
        lab_entry = ctk.CTkEntry(card, width=50, font=ctk.CTkFont(size=11))
        lab_entry.insert(0, str(info['horas_lab']))
        lab_entry.grid(row=2, column=2, padx=5, pady=5)
        
        # Distribución
        dist_label = ctk.CTkLabel(
            card,
            text=f"📊 {info['horas_teoria']}+{info['horas_lab']}",
            font=ctk.CTkFont(size=10),
            text_color="lightblue"
        )
        dist_label.grid(row=1, column=3, rowspan=2, padx=10, pady=5)
        
        self.widgets_materias[materia] = {
            'teoria_entry': teoria_entry,
            'lab_entry': lab_entry,
            'distribucion_label': dist_label,
            'total_horas': info['total_horas']
        }
        
        teoria_entry.bind('<KeyRelease>', lambda e, m=materia: self.actualizar_distribucion(m))
        lab_entry.bind('<KeyRelease>', lambda e, m=materia: self.actualizar_distribucion(m))
    
    def crear_tab_preferencias(self):
        """Crea la pestaña de preferencias de profesores"""
        tab = self.tabview.tab("👨‍🏫 Preferencias")
        
        # Instrucciones
        info_frame = ctk.CTkFrame(tab, fg_color="transparent")
        info_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            info_frame,
            text="💡 Configura preferencias de salones para cada profesor",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text="• Prioritario: El profesor DEBE usar ese salón (restricción fuerte)\n• Opcional: Preferencia sugerida (puede ignorarse si es necesario)",
            font=ctk.CTkFont(size=10),
            text_color="gray",
            justify="left"
        ).pack(anchor="w", pady=(5, 0))
        
        # Scrollable frame
        scrollable = ctk.CTkScrollableFrame(
            tab,
            label_text=f"Profesores ({len(self.profesores)})",
            label_font=ctk.CTkFont(size=16, weight="bold")
        )
        scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.widgets_preferencias = {}
        
        for profesor in self.profesores:
            self.crear_tarjeta_preferencia(scrollable, profesor)
    
    def crear_tarjeta_preferencia(self, parent, profesor):
        """Crea tarjeta de preferencias para un profesor"""
        card = ctk.CTkFrame(parent)
        card.pack(fill="x", padx=10, pady=5)
        
        # Nombre del profesor
        ctk.CTkLabel(
            card,
            text=profesor,
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 5), sticky="w")
        
        # Preferencia de salón teoría
        ctk.CTkLabel(card, text="🏫 Salón Teoría:", font=ctk.CTkFont(size=10)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        salon_teoria_var = ctk.StringVar(value=self.preferencias_profesores.get(profesor, {}).get('salon_teoria', 'Sin preferencia'))
        salon_teoria_menu = ctk.CTkOptionMenu(
            card,
            variable=salon_teoria_var,
            values=['Sin preferencia'] + self.salones_teoria,
            width=120,
            font=ctk.CTkFont(size=10)
        )
        salon_teoria_menu.grid(row=1, column=1, padx=5, pady=5)
        
        # Prioridad teoría
        prioridad_teoria_var = ctk.StringVar(value=self.preferencias_profesores.get(profesor, {}).get('prioridad_teoria', 'Opcional'))
        prioridad_teoria_menu = ctk.CTkOptionMenu(
            card,
            variable=prioridad_teoria_var,
            values=['Opcional', 'Prioritario'],
            width=100,
            font=ctk.CTkFont(size=10)
        )
        prioridad_teoria_menu.grid(row=1, column=2, padx=5, pady=5)
        
        # Preferencia de laboratorio
        ctk.CTkLabel(card, text="🔬 Laboratorio:", font=ctk.CTkFont(size=10)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        salon_lab_var = ctk.StringVar(value=self.preferencias_profesores.get(profesor, {}).get('salon_lab', 'Sin preferencia'))
        salon_lab_menu = ctk.CTkOptionMenu(
            card,
            variable=salon_lab_var,
            values=['Sin preferencia'] + self.salones_lab,
            width=120,
            font=ctk.CTkFont(size=10)
        )
        salon_lab_menu.grid(row=2, column=1, padx=5, pady=5)
        
        # Prioridad lab
        prioridad_lab_var = ctk.StringVar(value=self.preferencias_profesores.get(profesor, {}).get('prioridad_lab', 'Opcional'))
        prioridad_lab_menu = ctk.CTkOptionMenu(
            card,
            variable=prioridad_lab_var,
            values=['Opcional', 'Prioritario'],
            width=100,
            font=ctk.CTkFont(size=10)
        )
        prioridad_lab_menu.grid(row=2, column=2, padx=5, pady=5)
        
        self.widgets_preferencias[profesor] = {
            'salon_teoria_var': salon_teoria_var,
            'prioridad_teoria_var': prioridad_teoria_var,
            'salon_lab_var': salon_lab_var,
            'prioridad_lab_var': prioridad_lab_var
        }
    
    def actualizar_distribucion(self, materia):
        """Actualiza la etiqueta de distribución"""
        widgets = self.widgets_materias[materia]
        
        try:
            teoria = int(widgets['teoria_entry'].get() or 0)
            lab = int(widgets['lab_entry'].get() or 0)
            total = widgets['total_horas']
            
            if teoria + lab == total:
                widgets['distribucion_label'].configure(
                    text=f"✅ {teoria}+{lab}",
                    text_color="lightgreen"
                )
            else:
                widgets['distribucion_label'].configure(
                    text=f"⚠️ {teoria}+{lab} (≠{total})",
                    text_color="orange"
                )
        except ValueError:
            widgets['distribucion_label'].configure(
                text="❌ Error",
                text_color="red"
            )
    
    def guardar_todo(self):
        """Guarda materias y preferencias"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Guardar materias
            config_materias = {}
            errores = []
            
            for materia, widgets in self.widgets_materias.items():
                try:
                    teoria = int(widgets['teoria_entry'].get())
                    lab = int(widgets['lab_entry'].get())
                    total = widgets['total_horas']
                    
                    if teoria + lab != total:
                        errores.append(f"{materia}: {teoria}+{lab} ≠ {total}")
                        continue
                    
                    config_materias[materia] = {
                        'total_horas': total,
                        'horas_teoria': teoria,
                        'horas_lab': lab,
                        'distribucion': f"{teoria}+{lab}"
                    }
                except ValueError:
                    errores.append(f"{materia}: valores inválidos")
            
            if errores:
                messagebox.showwarning(
                    "Errores en Materias",
                    f"Se encontraron {len(errores)} errores:\n\n" + "\n".join(errores[:5])
                )
                return
            
            # Guardar preferencias
            config_preferencias = {}
            
            for profesor, widgets in self.widgets_preferencias.items():
                salon_teoria = widgets['salon_teoria_var'].get()
                prioridad_teoria = widgets['prioridad_teoria_var'].get()
                salon_lab = widgets['salon_lab_var'].get()
                prioridad_lab = widgets['prioridad_lab_var'].get()
                
                # Solo guardar si hay preferencia
                if salon_teoria != 'Sin preferencia' or salon_lab != 'Sin preferencia':
                    config_preferencias[profesor] = {
                        'salon_teoria': salon_teoria,
                        'prioridad_teoria': prioridad_teoria,
                        'salon_lab': salon_lab,
                        'prioridad_lab': prioridad_lab
                    }
            
            # Guardar archivos
            with open(os.path.join(script_dir, "configuracion_materias.json"), 'w', encoding='utf-8') as f:
                json.dump(config_materias, f, indent=2, ensure_ascii=False)
            
            with open(os.path.join(script_dir, "preferencias_profesores.json"), 'w', encoding='utf-8') as f:
                json.dump(config_preferencias, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo(
                "Éxito",
                f"✅ Configuración guardada\n\n"
                f"• {len(config_materias)} materias\n"
                f"• {len(config_preferencias)} profesores con preferencias"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{e}")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas generales"""
        try:
            # Stats materias
            total_materias = len(self.widgets_materias)
            solo_teoria = sum(1 for m, w in self.widgets_materias.items() 
                            if int(w['lab_entry'].get() or 0) == 0)
            solo_lab = sum(1 for m, w in self.widgets_materias.items() 
                          if int(w['teoria_entry'].get() or 0) == 0)
            mixtas = total_materias - solo_teoria - solo_lab
            
            # Stats preferencias
            total_profs = len(self.widgets_preferencias)
            con_pref_teoria = sum(1 for p, w in self.widgets_preferencias.items() 
                                 if w['salon_teoria_var'].get() != 'Sin preferencia')
            con_pref_lab = sum(1 for p, w in self.widgets_preferencias.items() 
                              if w['salon_lab_var'].get() != 'Sin preferencia')
            prioritarios = sum(1 for p, w in self.widgets_preferencias.items() 
                             if w['prioridad_teoria_var'].get() == 'Prioritario' or 
                                w['prioridad_lab_var'].get() == 'Prioritario')
            
            stats_text = f"""
📊 ESTADÍSTICAS GENERALES

📚 MATERIAS ({total_materias}):
  🏫 Solo teoría: {solo_teoria} ({solo_teoria/total_materias*100:.1f}%)
  🔬 Solo lab: {solo_lab} ({solo_lab/total_materias*100:.1f}%)
  🔄 Mixtas: {mixtas} ({mixtas/total_materias*100:.1f}%)

👨‍🏫 PROFESORES ({total_profs}):
  🏫 Con pref. teoría: {con_pref_teoria}
  🔬 Con pref. lab: {con_pref_lab}
  ⚠️  Prioritarios: {prioritarios}
            """
            
            messagebox.showinfo("Estadísticas", stats_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron calcular estadísticas:\n{e}")

if __name__ == "__main__":
    app = ConfiguradorISC()
    app.mainloop()
