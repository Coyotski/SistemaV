import csv
import re
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog

class VedasPesquerasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Consulta de Vedas Pesqueras en México")
        self.root.geometry("900x700")
        
        # Variables
        self.datos = []
        self.resultados_actuales = []
        self.archivo_csv = ""
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear interfaz
        self.setup_ui()
        
        # Solicitar archivo CSV al iniciar
        self.solicitar_archivo_csv()
    
    def setup_styles(self):
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 11, 'bold'))
        style.configure('Red.TButton', foreground='red')
    
    def setup_ui(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título y selección de archivo
        self.title_frame = ttk.Frame(self.main_frame)
        self.title_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.title_label = ttk.Label(
            self.title_frame, 
            text="CONSULTA DE VEDAS PESQUERAS EN MÉXICO", 
            style='Title.TLabel'
        )
        self.title_label.pack(side=tk.LEFT)
        
        self.btn_cambiar_archivo = ttk.Button(
            self.title_frame,
            text="Cambiar archivo CSV",
            command=self.solicitar_archivo_csv,
            style='Red.TButton'
        )
        self.btn_cambiar_archivo.pack(side=tk.RIGHT)
        
        # Mostrar archivo actual
        self.archivo_label = ttk.Label(
            self.main_frame,
            text="Archivo actual: Ninguno seleccionado",
            font=('Arial', 9)
        )
        self.archivo_label.pack(anchor=tk.W)
        
        # Notebook para las diferentes consultas
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de consulta por tipo
        self.tipo_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tipo_frame, text="Por Tipo de Veda")
        self.setup_tipo_ui()
        
        # Pestaña de consulta por fecha
        self.fecha_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.fecha_frame, text="Por Fecha")
        self.setup_fecha_ui()
        
        # Pestaña de consulta por especie
        self.especie_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.especie_frame, text="Por Especie")
        self.setup_especie_ui()
        
        # Área de resultados
        self.resultados_frame = ttk.Frame(self.main_frame)
        self.resultados_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        self.resultados_label = ttk.Label(
            self.resultados_frame, 
            text="Resultados:", 
            style='Header.TLabel'
        )
        self.resultados_label.pack(anchor=tk.W)
        
        self.resultados_text = scrolledtext.ScrolledText(
            self.resultados_frame,
            wrap=tk.WORD,
            width=80,
            height=15,
            font=('Arial', 10)
        )
        self.resultados_text.pack(fill=tk.BOTH, expand=True)
        
        # Botón de exportar
        self.exportar_btn = ttk.Button(
            self.main_frame,
            text="Exportar Resultados",
            command=self.exportar_resultados
        )
        self.exportar_btn.pack(pady=(10, 0))
        
        # Barra de estado
        self.status_var = tk.StringVar()
        self.status_var.set("Seleccione un archivo CSV para comenzar")
        self.status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN
        )
        self.status_bar.pack(fill=tk.X)
        
        # Deshabilitar controles hasta que se cargue un archivo
        self.set_controles_habilitados(False)
    
    def set_controles_habilitados(self, habilitado):
        """Habilita o deshabilita los controles según si hay archivo cargado"""
        state = 'normal' if habilitado else 'disabled'
        
        # Habilitar/deshabilitar todas las pestañas
        for tab in [self.tipo_frame, self.fecha_frame, self.especie_frame]:
            for child in tab.winfo_children():
                try:
                    child.configure(state=state)
                except:
                    pass  # Algunos widgets no tienen opción state
        
        self.exportar_btn.config(state=state)
    
    def solicitar_archivo_csv(self):
        archivo = filedialog.askopenfilename(
            title="Seleccione el archivo CSV de vedas pesqueras",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            self.archivo_csv = archivo
            self.archivo_label.config(text=f"Archivo actual: {os.path.basename(archivo)}")
            self.cargar_datos()
    
    def setup_tipo_ui(self):
        ttk.Label(
            self.tipo_frame, 
            text="Seleccione el tipo de veda a consultar:"
        ).pack(pady=(10, 5))
        
        self.tipo_var = tk.StringVar()
        
        self.rb_temporal = ttk.Radiobutton(
            self.tipo_frame,
            text="Vedas Temporales",
            variable=self.tipo_var,
            value="temporal"
        )
        self.rb_temporal.pack(anchor=tk.W, padx=20, pady=2)
        
        self.rb_permanente = ttk.Radiobutton(
            self.tipo_frame,
            text="Vedas Permanentes",
            variable=self.tipo_var,
            value="permanente"
        )
        self.rb_permanente.pack(anchor=tk.W, padx=20, pady=2)
        
        self.btn_consultar_tipo = ttk.Button(
            self.tipo_frame,
            text="Consultar",
            command=self.consultar_por_tipo
        )
        self.btn_consultar_tipo.pack(pady=10)
    
    def setup_fecha_ui(self):
        ttk.Label(
            self.fecha_frame,
            text="Seleccione el tipo de consulta por fecha:"
        ).pack(pady=(10, 5))
        
        self.fecha_var = tk.StringVar(value="dia")
        
        self.rb_dia = ttk.Radiobutton(
            self.fecha_frame,
            text="Consultar por día específico (DD/MM)",
            variable=self.fecha_var,
            value="dia"
        )
        self.rb_dia.pack(anchor=tk.W, padx=20, pady=2)
        
        self.rb_rango = ttk.Radiobutton(
            self.fecha_frame,
            text="Consultar por rango de fechas (DD/MM)",
            variable=self.fecha_var,
            value="rango"
        )
        self.rb_rango.pack(anchor=tk.W, padx=20, pady=2)
        
        # Frame para entrada de fecha
        self.fecha_input_frame = ttk.Frame(self.fecha_frame)
        self.fecha_input_frame.pack(pady=5)
        
        ttk.Label(
            self.fecha_input_frame, 
            text="Fecha:"
        ).grid(row=0, column=0, padx=5, pady=5)
        
        self.fecha_entry = ttk.Entry(
            self.fecha_input_frame, 
            width=10
        )
        self.fecha_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.lbl_fecha_fin = ttk.Label(
            self.fecha_input_frame, 
            text="Fecha fin:"
        )
        self.lbl_fecha_fin.grid(row=0, column=2, padx=5, pady=5)
        
        self.fecha_fin_entry = ttk.Entry(
            self.fecha_input_frame, 
            width=10
        )
        self.fecha_fin_entry.grid(row=0, column=3, padx=5, pady=5)
        self.fecha_fin_entry.grid_remove()
        self.lbl_fecha_fin.grid_remove()
        
        self.btn_consultar_fecha = ttk.Button(
            self.fecha_frame,
            text="Consultar",
            command=self.consultar_por_fecha
        )
        self.btn_consultar_fecha.pack(pady=10)
        
        # Actualizar UI según selección
        self.fecha_var.trace_add('write', self.actualizar_fecha_ui)
    
    def actualizar_fecha_ui(self, *args):
        if self.fecha_var.get() == "dia":
            self.fecha_fin_entry.grid_remove()
            self.lbl_fecha_fin.grid_remove()
        else:
            self.fecha_fin_entry.grid()
            self.lbl_fecha_fin.grid()
    
    def setup_especie_ui(self):
        ttk.Label(
            self.especie_frame,
            text="Seleccione el tipo de consulta por especie:"
        ).pack(pady=(10, 5))
        
        self.especie_var = tk.StringVar(value="comun")
        
        self.rb_comun = ttk.Radiobutton(
            self.especie_frame,
            text="Buscar por nombre común",
            variable=self.especie_var,
            value="comun"
        )
        self.rb_comun.pack(anchor=tk.W, padx=20, pady=2)
        
        self.rb_cientifico = ttk.Radiobutton(
            self.especie_frame,
            text="Buscar por nombre científico",
            variable=self.especie_var,
            value="cientifico"
        )
        self.rb_cientifico.pack(anchor=tk.W, padx=20, pady=2)
        
        ttk.Label(
            self.especie_frame,
            text="Término de búsqueda:"
        ).pack(pady=(5, 0))
        
        self.especie_entry = ttk.Entry(
            self.especie_frame, 
            width=40
        )
        self.especie_entry.pack(pady=5)
        
        self.btn_consultar_especie = ttk.Button(
            self.especie_frame,
            text="Consultar",
            command=self.consultar_por_especie
        )
        self.btn_consultar_especie.pack(pady=10)
    
    def procesar_fecha(self, texto_fecha):
        if "permanente" in texto_fecha.lower():
            return None
        
        fechas = re.findall(
            r'(\d{1,2})\s+de\s+([a-zA-Z]+)\s*(?:al|y del|y)\s*(\d{1,2})?\s*(?:de\s+([a-zA-Z]+))?', 
            texto_fecha, 
            re.IGNORECASE
        )
        
        meses = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
            'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }
        
        periodos = []
        for match in fechas:
            dia_inicio = int(match[0])
            mes_inicio = meses[match[1].lower()]
            dia_fin = int(match[2]) if match[2] else dia_inicio
            mes_fin = meses[match[3].lower()] if match[3] else mes_inicio
            
            año_actual = datetime.now().year
            fecha_inicio = datetime(año_actual, mes_inicio, dia_inicio)
            fecha_fin = datetime(año_actual, mes_fin, dia_fin)
            
            periodos.append((fecha_inicio, fecha_fin))
        
        return periodos
    
    def cargar_datos(self):
        if not self.archivo_csv:
            return
        
        self.status_var.set(f"Cargando {os.path.basename(self.archivo_csv)}...")
        self.root.update()
        
        try:
            with open(self.archivo_csv, mode='r', encoding='utf-8-sig') as file:
                # Verificar que el archivo tenga las columnas esperadas
                reader = csv.DictReader(file)
                campos_requeridos = {'ESPECIE', 'NOMBRE CIENTIFICO', 'ZONA', 'PERIODO'}
                
                if not campos_requeridos.issubset(reader.fieldnames):
                    raise ValueError("El archivo CSV no tiene el formato esperado")
                
                file.seek(0)
                next(reader)  # Saltar encabezados
                
                self.datos = []
                for i, row in enumerate(reader, 1):
                    periodos = self.procesar_fecha(row['PERIODO'])
                    row['PERIODOS'] = periodos
                    self.datos.append(row)
                
                self.status_var.set(f"{len(self.datos)} registros cargados correctamente")
                self.set_controles_habilitados(True)
                messagebox.showinfo(
                    "Carga completada", 
                    f"Se cargaron {len(self.datos)} registros desde:\n{os.path.basename(self.archivo_csv)}"
                )
                
        except Exception as e:
            messagebox.showerror(
                "Error al cargar archivo", 
                f"No se pudo cargar el archivo:\n{str(e)}\n"
                f"Por favor seleccione un archivo CSV válido con el formato correcto."
            )
            self.status_var.set("Error al cargar archivo")
            self.set_controles_habilitados(False)
    
    def mostrar_resultados(self, resultados):
        self.resultados_actuales = resultados
        self.resultados_text.config(state=tk.NORMAL)
        self.resultados_text.delete(1.0, tk.END)
        
        if not resultados:
            self.resultados_text.insert(tk.END, "\nNo se encontraron resultados.\n")
            self.resultados_text.config(state=tk.DISABLED)
            return
        
        for i, registro in enumerate(resultados, 1):
            self.resultados_text.insert(tk.END, f"\nREGISTRO {i}:\n")
            self.resultados_text.insert(tk.END, f"Especie: {registro['ESPECIE']}\n")
            self.resultados_text.insert(tk.END, f"Nombre científico: {registro['NOMBRE CIENTIFICO']}\n")
            self.resultados_text.insert(tk.END, f"Zona: {registro['ZONA']}\n")
            self.resultados_text.insert(tk.END, f"Periodo de veda: {registro['PERIODO']}\n")
            self.resultados_text.insert(tk.END, "-" * 80 + "\n")
        
        self.resultados_text.insert(tk.END, f"\nTotal de registros encontrados: {len(resultados)}\n")
        self.resultados_text.config(state=tk.DISABLED)
    
    def consultar_por_tipo(self):
        tipo = self.tipo_var.get()
        
        if not tipo:
            messagebox.showwarning("Advertencia", "Seleccione un tipo de veda")
            return
        
        self.status_var.set(f"Buscando vedas {'temporales' if tipo == 'temporal' else 'permanentes'}...")
        self.root.update()
        
        if tipo == "temporal":
            resultados = [r for r in self.datos if not r['PERIODO'].lower().startswith('permanente')]
        else:
            resultados = [r for r in self.datos if r['PERIODO'].lower().startswith('permanente')]
        
        self.mostrar_resultados(resultados)
        self.status_var.set(f"Encontrados {len(resultados)} registros")
    
    def consultar_por_fecha(self):
        tipo = self.fecha_var.get()
        
        try:
            if tipo == "dia":
                fecha_str = self.fecha_entry.get()
                dia, mes = map(int, fecha_str.split('/'))
                año_actual = datetime.now().year
                fecha_consulta = datetime(año_actual, mes, dia)
                
                resultados = []
                for registro in self.datos:
                    if registro['PERIODOS'] is None:
                        continue
                    
                    for periodo in registro['PERIODOS']:
                        fecha_inicio, fecha_fin = periodo
                        if fecha_inicio <= fecha_consulta <= fecha_fin:
                            resultados.append(registro)
                            break
                
                self.mostrar_resultados(resultados)
                self.status_var.set(f"Encontrados {len(resultados)} registros para {fecha_str}")
                
            else:  # rango
                inicio_str = self.fecha_entry.get()
                fin_str = self.fecha_fin_entry.get()
                
                dia_inicio, mes_inicio = map(int, inicio_str.split('/'))
                dia_fin, mes_fin = map(int, fin_str.split('/'))
                año_actual = datetime.now().year
                
                fecha_inicio_consulta = datetime(año_actual, mes_inicio, dia_inicio)
                fecha_fin_consulta = datetime(año_actual, mes_fin, dia_fin)
                
                resultados = []
                for registro in self.datos:
                    if registro['PERIODOS'] is None:
                        continue
                    
                    for periodo in registro['PERIODOS']:
                        fecha_inicio, fecha_fin = periodo
                        if not (fecha_fin < fecha_inicio_consulta or fecha_inicio > fecha_fin_consulta):
                            resultados.append(registro)
                            break
                
                self.mostrar_resultados(resultados)
                self.status_var.set(f"Encontrados {len(resultados)} registros entre {inicio_str} y {fin_str}")
                
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Use DD/MM.")
            self.status_var.set("Error en formato de fecha")
    
    def consultar_por_especie(self):
        tipo = self.especie_var.get()
        busqueda = self.especie_entry.get().strip()
        
        if not busqueda:
            messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda")
            return
        
        self.status_var.set(f"Buscando '{busqueda}'...")
        self.root.update()
        
        if tipo == "comun":
            resultados = [r for r in self.datos if busqueda.lower() in r['ESPECIE'].lower()]
        else:
            resultados = [r for r in self.datos if busqueda.lower() in r['NOMBRE CIENTIFICO'].lower()]
        
        self.mostrar_resultados(resultados)
        self.status_var.set(f"Encontrados {len(resultados)} registros")
    
    def exportar_resultados(self):
        if not self.resultados_actuales:
            messagebox.showwarning("Advertencia", "No hay resultados para exportar")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            title="Guardar resultados como"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("=" * 100 + "\n")
                file.write("RESULTADOS DE CONSULTA DE VEDAS PESQUERAS\n")
                file.write(f"Archivo fuente: {self.archivo_csv}\n")
                file.write("=" * 100 + "\n\n")
                
                for i, registro in enumerate(self.resultados_actuales, 1):
                    file.write(f"REGISTRO {i}:\n")
                    file.write(f"Especie: {registro['ESPECIE']}\n")
                    file.write(f"Nombre científico: {registro['NOMBRE CIENTIFICO']}\n")
                    file.write(f"Zona: {registro['ZONA']}\n")
                    file.write(f"Periodo de veda: {registro['PERIODO']}\n")
                    file.write("-" * 100 + "\n\n")
                
                file.write(f"Total de registros encontrados: {len(self.resultados_actuales)}\n")
            
            messagebox.showinfo("Éxito", f"Resultados exportados a:\n{file_path}")
            self.status_var.set("Resultados exportados")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar:\n{str(e)}")
            self.status_var.set("Error al exportar")

if __name__ == "__main__":
    root = tk.Tk()
    app = VedasPesquerasApp(root)
    root.mainloop()