
# ========= LIBRERIAS =============

from tkinter import ttk
import customtkinter as ctk
import ipaddress
from dataclasses import dataclass
from tkinter import font as tkFont
import sys

# =================================

@dataclass

# Definición de Estructuras de Datos para Resultados
# Aqui se toman los datos calculados y se almacenan en objetos para su posterior uso

class SubnetResult:
    name: str
    network: ipaddress.IPv4Network
    first_host: str
    last_host: str
    broadcast: str
    netmask: str
    cidr: str
    available_hosts: int
    required_hosts: int

# ========= CLASE PRINCIPAL DE LA CALCULADORA IP  =============

class CalculadoraIP:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title(" Calculadora IP - CIDR & VLSM")
        self.window.geometry("1300x800")
        self.window.minsize(1100, 700)
        
        self.current_theme = "dark"
        self.vlsm_rows = []
        self.next_row_id = 1
        self.results = []
        
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        
        self.setup_sidebar()
        self.setup_main_content()
        self.setup_status_bar()
        
        for _ in range(3):
            self.add_vlsm_row()
            
    # ======== INTERFAZ DE USUARIO  =============   
    
    # Configuración de la barra lateral de navegación
    def setup_sidebar(self):
        sidebar = ctk.CTkFrame(self.window, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 1))
        sidebar.grid_rowconfigure(8, weight=1)
        
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.pack(pady=(25, 10))
        
        logo = ctk.CTkLabel(
            logo_frame,
            text="🔧",
            font=ctk.CTkFont(size=42),
            text_color="#4CC9F0"
        )
        logo.pack()
        
        title = ctk.CTkLabel(
            logo_frame,
            text="Calculadora IP",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        title.pack()
        
        subtitle = ctk.CTkLabel(
            logo_frame,
            text="Por Rodriguez Paredes Roberto y Daniela Maldonado Bedolla",
            font=ctk.CTkFont(size=11),
            text_color="gray70"
        )
        subtitle.pack(pady=(2, 0))
        
        ctk.CTkFrame(sidebar, height=2, fg_color="gray30").pack(fill="x", padx=20, pady=20)
        
        nav_buttons = [
            ("1. CALCULADORA CIDR", self.show_cidr),
            ("2. CALCULADORA VLSM", self.show_vlsm),
            ("3. RESULTADOS", self.show_results),
        ]
        
        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                command=command,
                height=50,
                corner_radius=8,
                fg_color="transparent",
                hover_color="gray25",
                anchor="w",
                font=ctk.CTkFont(size=13)
            )
            btn.pack(fill="x", padx=15, pady=2)
        
        ctk.CTkFrame(sidebar, height=2, fg_color="gray30").pack(fill="x", padx=20, pady=25)
    
    # Configuración del contenido principal con pestañas
    def setup_main_content(self):

        self.main_container = ctk.CTkFrame(self.window, corner_radius=0)
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)
        
        self.tabview = ctk.CTkTabview(self.main_container, corner_radius=10)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        self.tabview.add("CIDR")
        self.tabview.add("VLSM")
        self.tabview.add("Resultados")
        
        self.setup_cidr_tab()
        self.setup_vlsm_tab()
        self.setup_results_tab()
        
        self.tabview.configure(state="normal")
    
    # Pestaña CIDR
    def setup_cidr_tab(self):
        tab = self.tabview.tab("CIDR")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        
        input_frame = ctk.CTkFrame(tab, corner_radius=10)
        input_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        input_frame.grid_columnconfigure(1, weight=1)
        
        title = ctk.CTkLabel(
            input_frame,
            text="Calculadora CIDR - Subneteo ",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#4CC9F0"
        )
        title.grid(row=0, column=0, columnspan=3, pady=(15, 25))
        
        ctk.CTkLabel(
            input_frame,
            text="Dirección IP de Red:",
            font=ctk.CTkFont(size=14)
        ).grid(row=1, column=0, sticky="w", padx=20, pady=10)
        
        self.cidr_ip_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Ej: 192.168.1.0",
            height=40,
            corner_radius=8
        )
        self.cidr_ip_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.cidr_ip_entry.insert(0, "192.168.1.0")
        
        mask_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        mask_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        self.cidr_mask_type = ctk.StringVar(value="cidr")
        
        ctk.CTkLabel(
            mask_frame,
            text="Formato:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkRadioButton(
            mask_frame,
            text="CIDR ( ej: /24 )",
            variable=self.cidr_mask_type,
            value="cidr",
            command=self.on_cidr_mask_change
        ).pack(side="left", padx=5)
        
        ctk.CTkRadioButton(
            mask_frame,
            text="Máscara ( ej: 255.255.255.0 )",
            variable=self.cidr_mask_type,
            value="mask",
            command=self.on_cidr_mask_change
        ).pack(side="left", padx=5)
        
        mask_input_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        mask_input_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        self.cidr_cidr_entry = ctk.CTkEntry(
            mask_input_frame,
            placeholder_text="/24",
            width=100,
            height=40,
            corner_radius=8
        )
        self.cidr_cidr_entry.pack(side="left")
        self.cidr_cidr_entry.insert(0, "24")
        
        self.cidr_mask_entry = ctk.CTkEntry(
            mask_input_frame,
            placeholder_text="255.255.255.0",
            width=180,
            height=40,
            corner_radius=8,
            state="disabled"
        )
        self.cidr_mask_entry.pack(side="left", padx=(10, 0))
        self.cidr_mask_entry.insert(0, "255.255.255.0")
        
        calc_btn = ctk.CTkButton(
            input_frame,
            text="CALCULAR SUBNET",
            command=self.calculate_cidr,
            height=45,
            corner_radius=10,
            fg_color="#4361EE",
            hover_color="#3A56D4",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        calc_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        results_frame = ctk.CTkFrame(tab, corner_radius=10)
        results_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            results_frame,
            text="Resultados Detallados",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#4CC9F0"
        ).grid(row=0, column=0, pady=15)
        
        columns = ["Propiedad", "Valor", "Binario"]
        self.cidr_tree = ttk.Treeview(
            results_frame,
            columns=columns,
            show="headings",
            height=14,
            style="Custom.Treeview"
        )
        
        col_widths = [180, 200, 250]
        for col, width in zip(columns, col_widths):
            self.cidr_tree.heading(col, text=col)
            self.cidr_tree.column(col, width=width, anchor="w")
        
        scroll_y = ttk.Scrollbar(results_frame, orient="vertical", command=self.cidr_tree.yview)
        scroll_x = ttk.Scrollbar(results_frame, orient="horizontal", command=self.cidr_tree.xview)
        self.cidr_tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.cidr_tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        scroll_y.grid(row=1, column=1, sticky="ns")
        scroll_x.grid(row=2, column=0, sticky="ew")
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview",
                       background="#2b2b2b",
                       foreground="white",
                       fieldbackground="#2b2b2b",
                       borderwidth=0)
        style.configure("Custom.Treeview.Heading",
                       background="#3a3a3a",
                       foreground="white",
                       relief="flat")
        style.map("Custom.Treeview", background=[("selected", "#3A56D4")])
    
    # Pestaña VLSM
    def setup_vlsm_tab(self):
        tab = self.tabview.tab("VLSM")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        
        config_frame = ctk.CTkFrame(tab, corner_radius=10)
        config_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        config_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            config_frame,
            text="Calculadora VLSM - Subneteo Variable",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#4CC9F0"
        ).grid(row=0, column=0, columnspan=3, pady=(15, 20))
        
        ctk.CTkLabel(
            config_frame,
            text="Red Principal:",
            font=ctk.CTkFont(size=14)
        ).grid(row=1, column=0, sticky="w", padx=20, pady=10)
        
        self.vlsm_network_entry = ctk.CTkEntry(
            config_frame,
            placeholder_text="Ej: 192.168.0.0/24",
            height=40,
            corner_radius=8
        )
        self.vlsm_network_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.vlsm_network_entry.insert(0, "192.168.0.0/24")
        
        quick_net_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        quick_net_frame.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        
        ctk.CTkLabel(quick_net_frame, text="CIDR:").pack(side="left", padx=(0, 5))
        
        quick_nets = ["/24", "/16", "/8"]
        for net in quick_nets:
            btn = ctk.CTkButton(
                quick_net_frame,
                text=net,
                width=40,
                height=30,
                command=lambda n=net: self.set_quick_network(n),
                fg_color="gray30",
                hover_color="gray40"
            )
            btn.pack(side="left", padx=2)
        
        req_frame = ctk.CTkFrame(tab, corner_radius=10)
        req_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        req_frame.grid_columnconfigure(0, weight=1)
        req_frame.grid_rowconfigure(1, weight=1)
        
        header_frame = ctk.CTkFrame(req_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            header_frame,
            text="Requisitos de Subredes",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, sticky="w")
        
        controls_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        controls_frame.grid(row=0, column=1, sticky="e")
        
        # Botones para gestionar filas
        control_buttons = [
            ("➕ Añadir Fila", self.add_vlsm_row, "#38B000"),
            ("➖ Eliminar Fila", self.remove_vlsm_row, "#E71D36"),
            ("🧹 Limpiar", self.clear_vlsm_rows, "#FF9500")
        ]
        
        for text, command, color in control_buttons:
            btn = ctk.CTkButton(
                controls_frame,
                text=text,
                command=command,
                width=110,
                height=35,
                corner_radius=8,
                fg_color=color,
                hover_color=self.darken_color(color),
                font=ctk.CTkFont(size=12)
            )
            btn.pack(side="left", padx=5)
        
        self.vlsm_rows_container = ctk.CTkScrollableFrame(
            req_frame,
            corner_radius=8,
            height=200
        )
        self.vlsm_rows_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.vlsm_rows_container.grid_columnconfigure(0, weight=1)
        
        headers_frame = ctk.CTkFrame(self.vlsm_rows_container, fg_color="#3a3a3a", height=40)
        headers_frame.pack(fill="x", pady=(0, 5))
        
        headers = ["ID", "Nombre Subred", "Hosts Requeridos", "Prioridad", "Acciones"]
        col_widths = [50, 200, 150, 100, 100]
        
        for i, (header, width) in enumerate(zip(headers, col_widths)):
            label = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=width
            )
            label.pack(side="left", padx=10, pady=10)
        
        action_frame = ctk.CTkFrame(tab, fg_color="transparent")
        action_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))
        
        calc_btn = ctk.CTkButton(
            action_frame,
            text=" CALCULAR VLSM ",
            command=self.calculate_vlsm,
            height=50,
            corner_radius=10,
            fg_color="#7209B7",
            hover_color="#5A0890",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        calc_btn.pack(pady=10)
        
        extra_btns_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        extra_btns_frame.pack(pady=5)
        
        extra_buttons = [
            (" Ver Tabla Completa ", self.show_full_table),
            (" Ordenar por Hosts ", self.sort_by_hosts)
        ]
        
        for text, command in extra_buttons:
            btn = ctk.CTkButton(
                extra_btns_frame,
                text=text,
                command=command,
                width=140,
                height=35,
                corner_radius=8,
                fg_color="gray30",
                hover_color="gray40"
            )
            btn.pack(side="left", padx=5)
    
    # Pestaña Resultados para VLSM
    def setup_results_tab(self):
        tab = self.tabview.tab("Resultados")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(tab, corner_radius=0)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1) 

        ctk.CTkLabel(
            main_frame,
            text="📊 Resultados de Cálculos",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#4CC9F0"
        ).grid(row=0, column=0, pady=(10, 20))

        stats_frame = ctk.CTkFrame(main_frame, corner_radius=12)
        stats_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 20))
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.stats_labels = {}
        stats_data = [
            (" Subredes", "subnets", "0"),
            (" Hosts Totales", "total_hosts", "0"),
            (" Asignados", "assigned_hosts", "0"),
            (" Disponibles", "available_hosts", "0"),
            (" Sin Asignar", "unassigned_hosts", "0"),
            (" Eficiencia", "efficiency", "0%")
        ]

        for i, (title, key, default) in enumerate(stats_data):
            card = ctk.CTkFrame(
                stats_frame,
                fg_color="gray18",
                corner_radius=12,
                height=100
            )
            card.grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky="ew")
            card.grid_propagate(False)

            ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=13),
                text_color="gray70"
            ).pack(pady=(18, 5))

            value = ctk.CTkLabel(
                card,
                text=default,
                font=ctk.CTkFont(size=22, weight="bold"),
                text_color="#4CC9F0"
            )
            value.pack()

            self.stats_labels[key] = value

        table_container = ctk.CTkFrame(main_frame, corner_radius=12)
        table_container.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 15))
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)

        columns = [
            "Subred", "IP de Red", "Máscara", "CIDR",
            "Rango de Hosts", "Broadcast",
            "Req.", "Disp.", "Uso %"
        ]

        self.results_tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings"
        )

        col_widths = [140, 130, 120, 70, 260, 130, 70, 70, 70]
        for col, width in zip(columns, col_widths):
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=width, anchor="center")

        scroll_y = ttk.Scrollbar(
            table_container, orient="vertical", command=self.results_tree.yview
        )
        scroll_x = ttk.Scrollbar(
            table_container, orient="horizontal", command=self.results_tree.xview
        )

        self.results_tree.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        self.results_tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.grid(row=3, column=0, pady=(0, 10))

        buttons = [
            ("📄 Exportar CSV", self.export_csv),
            ("🧹 Limpiar", self.clear_all)
        ]

        for text, command in buttons:
            ctk.CTkButton(
                buttons_frame,
                text=text,
                command=command,
                width=170,
                height=40,
                corner_radius=10
            ).pack(side="left", padx=8)

    # Configuración de la barra de estado para manejar errores y mostrar mensajes durante la ejecución
    def setup_status_bar(self):
        status_bar = ctk.CTkFrame(self.window, height=30, corner_radius=0)
        status_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 5))
        
        self.status_message = ctk.CTkLabel(
            status_bar,
            text=" Sistema listo. Ingrese los datos para calcular.",
            font=ctk.CTkFont(size=11)
        )
        self.status_message.pack(side="left", padx=10)
        
        self.row_counter = ctk.CTkLabel(
            status_bar,
            text="Subredes: 0",
            font=ctk.CTkFont(size=11),
            text_color="gray70"
        )
        self.row_counter.pack(side="right", padx=10)
    
    #  ===== FUNCIONES ADICIONALES PARA LA GESTIÓN DE FILAS EN VLSM =========
    
    def add_vlsm_row(self, name="", hosts=""):
        row_id = self.next_row_id
        self.next_row_id += 1
        
        row_frame = ctk.CTkFrame(self.vlsm_rows_container, height=45, fg_color="gray20", corner_radius=6)
        row_frame.pack(fill="x", pady=2)
        row_frame.pack_propagate(False)
        
        id_label = ctk.CTkLabel(
            row_frame,
            text=str(row_id),
            width=50,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#4CC9F0"
        )
        id_label.pack(side="left", padx=10)
        
        name_var = ctk.StringVar(value=name if name else f"Subred {row_id}")
        name_entry = ctk.CTkEntry(
            row_frame,
            textvariable=name_var,
            placeholder_text="Nombre de subred",
            width=200,
            height=35
        )
        name_entry.pack(side="left", padx=5)
        
        hosts_var = ctk.StringVar(value=hosts if hosts else str(row_id * 10))
        hosts_entry = ctk.CTkEntry(
            row_frame,
            textvariable=hosts_var,
            placeholder_text="Ej: 50",
            width=150,
            height=35
        )
        hosts_entry.pack(side="left", padx=5)
        
        priority_var = ctk.StringVar(value="Media")
        priority_combo = ctk.CTkComboBox(
            row_frame,
            values=["Alta", "Media", "Baja"],
            variable=priority_var,
            width=100,
            height=35,
            state="readonly"
        )
        priority_combo.pack(side="left", padx=5)
        
        action_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=100)
        action_frame.pack(side="left", padx=5)
        action_frame.pack_propagate(False)
        
        duplicate_btn = ctk.CTkButton(
            action_frame,
            text="⎘",
            width=30,
            height=30,
            command=lambda: self.duplicate_row(row_id),
            fg_color="gray40",
            hover_color="gray50",
            font=ctk.CTkFont(size=12)
        )
        duplicate_btn.pack(side="left", padx=2)
        
        delete_btn = ctk.CTkButton(
            action_frame,
            text="✕",
            width=30,
            height=30,
            command=lambda: self.delete_vlsm_row(row_id),
            fg_color="#E71D36",
            hover_color="#C1121F",
            font=ctk.CTkFont(size=12)
        )
        delete_btn.pack(side="left", padx=2)
        
        self.vlsm_rows.append({
            "id": row_id,
            "frame": row_frame,
            "name_var": name_var,
            "hosts_var": hosts_var,
            "priority_var": priority_var
        })
        
        self.update_row_counter()
    
    def duplicate_row(self, row_id):
        for row in self.vlsm_rows:
            if row["id"] == row_id:
                self.add_vlsm_row(
                    name=f"{row['name_var'].get()} (copia)",
                    hosts=row["hosts_var"].get()
                )
                break
    
    def delete_vlsm_row(self, row_id):
        for i, row in enumerate(self.vlsm_rows):
            if row["id"] == row_id:
                row["frame"].destroy()
                self.vlsm_rows.pop(i)
                self.update_row_counter()
                break
    
    def remove_vlsm_row(self):
        if self.vlsm_rows:
            row = self.vlsm_rows.pop()
            row["frame"].destroy()
            self.update_row_counter()
    
    def clear_vlsm_rows(self):
        for row in self.vlsm_rows:
            row["frame"].destroy()
        self.vlsm_rows.clear()
        self.next_row_id = 1
        self.update_row_counter()
        
        # Añadir 3 filas por defecto
        for _ in range(3):
            self.add_vlsm_row()
    
    def sort_by_hosts(self):
        try:
            rows_data = []
            for row in self.vlsm_rows:
                try:
                    hosts = int(row["hosts_var"].get())
                    rows_data.append((row, hosts))
                except:
                    rows_data.append((row, 0))
            
            rows_data.sort(key=lambda x: x[1], reverse=True)
            
            # Destruir frames existentes
            for row in self.vlsm_rows:
                row["frame"].destroy()
            
            self.vlsm_rows = []
            for row_data, _ in rows_data:
                self.add_vlsm_row(
                    row_data["name_var"].get(),
                    row_data["hosts_var"].get()
                )
            
            self.show_message(" Filas ordenadas por hosts", "success")
            
        except Exception as e:
            self.show_message(f"Error al ordenar: {str(e)}", "error")
    
    def update_row_counter(self):
        count = len(self.vlsm_rows)
        self.row_counter.configure(text=f"Subredes: {count}")
    
    #  ========================================================================
    
    
    # ======== FUNCIONES DE CÁLCULO PARA CIDR Y VLSM =============
    """"
    Funcion para calcular CIDR:
        Realiza cálculos de subneteo basados en la IP y máscara/CIDR proporcionados
        Devuelve detalles como dirección de red, broadcast, rango de hosts, etc.
        
        Proceso:
        
        1. Validar y parsear la IP y la máscara o prefijo CIDR.
        2. Calcular:
            - Dirección de red
            - Dirección de broadcast
            - Rango de hosts
            - Total de direcciones y hosts utilizables
        3. Determinar:
            - Clase de la red
            - Tipo de red (pública o privada)
        4. Mostrar los resultados en la tabla de CIDR.
        
    """
    def calculate_cidr(self):
        try:
            ip_str = self.cidr_ip_entry.get().strip()
            
            # 1. Verificar si el formato seleccionado es CID
            # 2. Obtener el prefijo CIDR ingresado por el usuario
            # 3. Asegurarse de que el prefijo CIDR comience con '/'
            # 4. Convertir el prefijo CIDR a un número entero
            
            if self.cidr_mask_type.get() == "cidr":
                cidr_str = self.cidr_cidr_entry.get().strip()
                if not cidr_str.startswith('/'):
                    cidr_str = '/' + cidr_str
                prefixlen = int(cidr_str[1:])
            else:
                mask_str = self.cidr_mask_entry.get().strip()
                # Convertir máscara a CIDR manualmente
                octets = mask_str.split('.')
                binary_str = ''.join([format(int(o), '08b') for o in octets])
                prefixlen = binary_str.count('1')
            
            # Validar el prefijo CIDR
            if not (0 <= prefixlen <= 32):
                raise ValueError("Prefijo CIDR debe estar entre 0 y 32")
            
            ip_octets = ip_str.split('.')
            if len(ip_octets) != 4:
                raise ValueError("Dirección IP inválida")
            
            ip_int = 0
            for i, octet in enumerate(ip_octets):
                octet_val = int(octet)
                if not (0 <= octet_val <= 255):
                    raise ValueError(f"Octeto {octet} fuera de rango")
                ip_int = (ip_int << 8) | octet_val
            
            # Calcular máscara de red
            mask_int = (0xFFFFFFFF << (32 - prefixlen)) & 0xFFFFFFFF
            
            # Dirección de red
            network_int = ip_int & mask_int
            
            # Dirección broadcast ( Se calcula con operación OR entre la red y el complemento de la máscara )
            broadcast_int = network_int | (~mask_int & 0xFFFFFFFF)
            
            # Total de direcciones ( Se calcula como 2^(32 - prefixlen) donde prefixlen es el prefijo CIDR )
            total_addresses = 1 << (32 - prefixlen)
            
            # Hosts utilizables y rango de hosts
            if prefixlen <= 30:
                usable_hosts = total_addresses - 2
                first_host = network_int + 1
                last_host = broadcast_int - 1
                ip_range = f"{self.int_to_ip(first_host)} - {self.int_to_ip(last_host)}"
            else:
                usable_hosts = total_addresses
                first_host = network_int
                last_host = broadcast_int
                ip_range = f"{self.int_to_ip(first_host)} - {self.int_to_ip(last_host)}"
            
            for item in self.cidr_tree.get_children():
                self.cidr_tree.delete(item)
            
            # Convertir a strings para mostrar
            network_str = self.int_to_ip(network_int)
            mask_str = self.int_to_ip(mask_int)
            broadcast_str = self.int_to_ip(broadcast_int)
            first_host_str = self.int_to_ip(first_host)
            last_host_str = self.int_to_ip(last_host)
            
            # Determinar clase de red mandando llamar a la clase get_ip_class_manual
            network_class = self.get_ip_class_manual(ip_int)
            
            # Determinar tipo de red mandando llamar a la clase get_network_type_manual
            network_type = self.get_network_type_manual(network_int)
            
            # Información para mostrar en la interfaz de la tabla
            info = [
                ("Dirección de Red", network_str, self.ip_to_binary(network_str)),
                ("Máscara de Red", mask_str, self.ip_to_binary(mask_str)),
                ("Notación CIDR", f"/{prefixlen}", bin(prefixlen)[2:].zfill(8)),
                ("Dirección Broadcast", broadcast_str, self.ip_to_binary(broadcast_str)),
                ("Total de Direcciones", str(total_addresses), bin(total_addresses)[2:]),
                ("Hosts Utilizables", str(usable_hosts), ""),
                ("Primer Host", first_host_str, ""),
                ("Último Host", last_host_str, ""),
                ("Rango de IPs", ip_range, ""),
                ("Clase de Red", network_class, ""),
                ("Tipo", network_type, ""),
            ]
            
            for prop, value, binary in info:
                self.cidr_tree.insert("", "end", values=(prop, value, binary))
            
            self.show_message(f" CIDR calculado: {network_str}/{prefixlen}", "success")
            self.tabview.set("Resultados")
            
        except Exception as e:
            self.show_message(f" Error: {str(e)}", "error")    

    """
    Funcion para calcular VLSM:
        Realiza cálculos de subneteo variable basados en la red principal y los requisitos de subredes.
        Devuelve detalles como direcciones de red, broadcast, rangos de hosts, máscaras para cada subred.
        
        Proceso:
        
        1. Validar y parsear la red principal (IP/CIDR).
        2. Obtener y validar los requisitos de subredes (nombre, hosts requeridos, prioridad).
        3. Ordenar los requisitos por número de hosts (descendente).
        4. Calcular subredes VLSM:
            - Determinar el tamaño adecuado para cada subred.
            - Calcular dirección de red, broadcast, rango de hosts, máscara, etc.
            - Verificar que no se exceda el espacio disponible en la red principal.
        5. Mostrar los resultados en la tabla de Resultados.
    
    """
    
    def calculate_vlsm(self):
        try:
            
            # Obtener red principal 
            network_str = self.vlsm_network_entry.get().strip()
            if '/' not in network_str:
                raise ValueError("Formato de red debe ser IP/CIDR (ej: 192.168.0.0/24)")
            
            ip_part, cidr_part = network_str.split('/')
            prefixlen = int(cidr_part)
            
            if not (0 <= prefixlen <= 32):
                raise ValueError("Prefijo CIDR debe estar entre 0 y 32")
            
            # Parsear IP base
            ip_octets = ip_part.split('.')
            if len(ip_octets) != 4:
                raise ValueError("Dirección IP inválida")
            
            base_ip_int = 0
            for i, octet in enumerate(ip_octets):
                octet_val = int(octet)
                if not (0 <= octet_val <= 255):
                    raise ValueError(f"Octeto {octet} fuera de rango")
                base_ip_int = (base_ip_int << 8) | octet_val
            
            # Calcular máscara de la red principal ( Se calcula con un corrimiento a la izquierda )
            main_mask_int = (0xFFFFFFFF << (32 - prefixlen)) & 0xFFFFFFFF
            network_int = base_ip_int & main_mask_int
            
            # Dirección broadcast de la red principal ( Se calcula con operación OR entre la red y el complemento de la máscara )
            broadcast_int = network_int | (~main_mask_int & 0xFFFFFFFF)
            
            # Obtener requisitos de subredes desde las filas ingresadas
            requirements = []
            for row in self.vlsm_rows:
                try:
                    hosts = int(row["hosts_var"].get())
                    if hosts > 0:
                        requirements.append({
                            "name": row["name_var"].get(),
                            "hosts": hosts,
                            "priority": row["priority_var"].get()
                        })
                except ValueError:
                    continue
            
            if not requirements:
                self.show_message(" Ingrese al menos un requisito válido", "warning")
                return
            
            # Ordenamos por hosts (descendente)
            requirements.sort(key=lambda x: x["hosts"], reverse=True)
            
            
            # Calcular hosts disponibles en la red principal
            total_hosts_main = (1 << (32 - prefixlen)) - 2

            # Calcular hosts requeridos
            total_required_hosts = sum(r["hosts"] for r in requirements)

            if total_required_hosts > total_hosts_main:
                self.show_message(
                    f"❌ Exceso de hosts: se requieren {total_required_hosts} "
                    f"pero la red solo soporta {total_hosts_main}",
                    "error"
                )
                return

            
            # Calculamos las suberdes VLSM
            self.results = []
            current_ip_int = network_int
            total_required = 0
            total_available = 0
            
            for req in requirements:
                # Calcular número de hosts necesarios (incluyendo red y broadcast)
                hosts_needed = req["hosts"]
                required_size = hosts_needed + 2  # +2 para dirección de red y broadcast
                
                # Encontrar el tamaño de subred adecuado (potencia de 2)
                subnet_size = 1
                subnet_prefix = 32
                
                while subnet_size < required_size and subnet_prefix > 0:
                    subnet_prefix -= 1
                    subnet_size <<= 1  # Multiplicar por 2
                
                # Verificar que la subred calculada pueda alojar los hosts necesarios
                if subnet_prefix < prefixlen:
                    self.show_message(f" No hay espacio para {req['name']} (necesita {hosts_needed} hosts)", "warning")
                    continue
                
                # Verificar que no nos pasemos del broadcast de la red principal
                subnet_broadcast_int = current_ip_int + subnet_size - 1
                
                if subnet_broadcast_int > broadcast_int:
                    self.show_message(f"Espacio insuficiente para {req['name']}", "warning")
                    break
                
                # Calcular máscara de esta subred
                subnet_mask_int = (0xFFFFFFFF << (32 - subnet_prefix)) & 0xFFFFFFFF
                
                # Calcular información de la subred 
                subnet_network_int = current_ip_int
                subnet_broadcast_int = subnet_network_int + subnet_size - 1
                
                if subnet_prefix <= 30:
                    first_host_int = subnet_network_int + 1
                    last_host_int = subnet_broadcast_int - 1
                    available_hosts = subnet_size - 2
                else:
                    first_host_int = subnet_network_int
                    last_host_int = subnet_broadcast_int
                    available_hosts = subnet_size
                
                # Guardar resultado de la subred
                self.results.append(SubnetResult(
                    name=req["name"],
                    network=self.create_network_obj_manual(subnet_network_int, subnet_prefix),
                    first_host=self.int_to_ip(first_host_int),
                    last_host=self.int_to_ip(last_host_int),
                    broadcast=self.int_to_ip(subnet_broadcast_int),
                    netmask=self.int_to_ip(subnet_mask_int),
                    cidr=f"/{subnet_prefix}",
                    available_hosts=available_hosts,
                    required_hosts=hosts_needed
                ))
                
                # Actualizar totales globales
                
                total_required += hosts_needed
                total_available += available_hosts
                
                # Mover al siguiente bloque
                current_ip_int = subnet_broadcast_int + 1
            
            # Actualizar interfaz
            self.update_results_display()
            self.update_stats(total_required, total_available)
            
            self.show_message(f" VLSM calculado: {len(self.results)} subredes creadas", "success")
            self.tabview.set("Resultados")
            
        except Exception as e:
            self.show_message(f" Error VLSM: {str(e)}", "error")
    
    # ===============================================================
    
    # ===== FUNCIONES AUXILIARES PARA CÁLCULOS DE IP ========
    
    def int_to_ip(self, ip_int):
        return f"{(ip_int >> 24) & 0xFF}.{(ip_int >> 16) & 0xFF}.{(ip_int >> 8) & 0xFF}.{ip_int & 0xFF}"

    def ip_to_int(self, ip_str):
        octets = ip_str.split('.')
        ip_int = 0
        for octet in octets:
            ip_int = (ip_int << 8) | int(octet)
        return ip_int

    def get_network_type_manual(self, ip_int):
        first_octet = (ip_int >> 24) & 0xFF
        second_octet = (ip_int >> 16) & 0xFF
        
        if first_octet == 10:  # 10.0.0.0/8
            return "Privada"
        elif first_octet == 172 and 16 <= second_octet <= 31:  # 172.16.0.0/12
            return "Privada"
        elif first_octet == 192 and second_octet == 168:  # 192.168.0.0/16
            return "Privada"
        # Direcciones de enlace local
        elif first_octet == 169 and second_octet == 254:  # 169.254.0.0/16
            return "Enlace Local"
        else:
            return "Pública"

    def create_network_obj_manual(self, network_int, prefixlen):
        # Crear una clase simple que simule ipaddress.IPv4Network
        class ManualNetwork:
            def __init__(self, network_int, prefixlen):
                self.network_address = self.int_to_ip(network_int)
                self.prefixlen = prefixlen
                
                # Calcular máscara
                mask_int = (0xFFFFFFFF << (32 - prefixlen)) & 0xFFFFFFFF
                self.netmask = self.int_to_ip(mask_int)
                
                # Calcular broadcast
                broadcast_int = network_int | (~mask_int & 0xFFFFFFFF)
                self.broadcast_address = self.int_to_ip(broadcast_int)
                
                # Calcular número total de direcciones
                self.num_addresses = 1 << (32 - prefixlen)
            
            def int_to_ip(self, ip_int):
                return f"{(ip_int >> 24) & 0xFF}.{(ip_int >> 16) & 0xFF}.{(ip_int >> 8) & 0xFF}.{ip_int & 0xFF}"
        
        return ManualNetwork(network_int, prefixlen)

    def get_ip_class_manual(self, ip_int):
        first_octet = (ip_int >> 24) & 0xFF
        
        if 1 <= first_octet <= 126:
            return "A"
        elif 128 <= first_octet <= 191:
            return "B"
        elif 192 <= first_octet <= 223:
            return "C"
        elif 224 <= first_octet <= 239:
            return "D (Multicast)"
        else:
            return "Desconocida"

    # ========================================================
    
    # ===== FUNCIONES DE INTERFAZ PARA RESULTADOS ========

    def update_results_display(self):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        for result in self.results:
            usage = f"{(result.required_hosts / result.available_hosts * 100):.1f}%" if result.available_hosts > 0 else "N/A"
            
            self.results_tree.insert("", "end", values=(
                result.name,
                str(result.network.network_address),
                result.netmask,
                result.cidr,
                f"{result.first_host} - {result.last_host}",
                result.broadcast,
                result.required_hosts,
                result.available_hosts,
                usage
            ))
    
    def update_stats(self, total_required, total_available):
        subnet_count = len(self.results)
        
        self.stats_labels["subnets"].configure(text=str(subnet_count))
        self.stats_labels["total_hosts"].configure(text=str(total_available + (subnet_count * 2)))
        self.stats_labels["assigned_hosts"].configure(text=str(total_required))
        
        if total_available > 0:
            efficiency = (total_required / total_available) * 100
            self.stats_labels["efficiency"].configure(text=f"{efficiency:.1f}%")
        else:
            self.stats_labels["efficiency"].configure(text="0%")
        
        self.stats_labels["available_hosts"].configure(text=str(total_available))
        
        unassigned = total_available - total_required
        self.stats_labels["unassigned_hosts"].configure(text=str(max(0, unassigned)))
    
    def show_full_table(self):
        if not self.results:
            self.show_message("⚠️ Calcule VLSM primero", "warning")
            return
        
        popup = ctk.CTkToplevel(self.window)
        popup.title(" Tabla Completa de Subredes")
        popup.geometry("900x600")
        
        # Título
        ctk.CTkLabel(
            popup,
            text="Tabla Detallada de Subredes VLSM",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        columns = ["Subred", "IP Red", "Máscara", "CIDR", "Primer Host", "Último Host", 
                  "Broadcast", "Hosts Req.", "Hosts Disp.", "Uso %"]
        
        tree = ttk.Treeview(popup, columns=columns, show="headings", height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        
        for result in self.results:
            usage = f"{(result.required_hosts / result.available_hosts * 100):.1f}" if result.available_hosts > 0 else "N/A"
            binary = self.ip_to_binary(str(result.network.network_address))
            
            tree.insert("", "end", values=(
                result.name,
                str(result.network.network_address),
                result.netmask,
                result.cidr,
                result.first_host,
                result.last_host,
                result.broadcast,
                result.required_hosts,
                result.available_hosts,
                usage,
                binary
            ))
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(popup, orient="vertical", command=tree.yview)
        scroll_x = ttk.Scrollbar(popup, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
    
    def export_csv(self):
        try:
            from tkinter import filedialog
            import csv
            
            if not self.results:
                self.show_message("⚠️ No hay resultados para exportar", "warning")
                return
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Subred", "IP Red", "Máscara", "CIDR", "Primer Host", 
                                   "Último Host", "Broadcast", "Hosts Req.", "Hosts Disp.", "Uso %"])
                    
                    for result in self.results:
                        usage = f"{(result.required_hosts / result.available_hosts * 100):.1f}" if result.available_hosts > 0 else "N/A"
                        writer.writerow([
                            result.name,
                            str(result.network.network_address),
                            result.netmask,
                            result.cidr,
                            result.first_host,
                            result.last_host,
                            result.broadcast,
                            result.required_hosts,
                            result.available_hosts,
                            usage
                        ])
                
                self.show_message(f"✅ Resultados exportados a {filename}", "success")
                
        except Exception as e:
            self.show_message(f"❌ Error al exportar: {str(e)}", "error")
    
    # =========================================================
    
    # ===== FUNCIONES AUXILIARES DE INTERFAZ ========
    
    def on_cidr_mask_change(self):
        if self.cidr_mask_type.get() == "cidr":
            self.cidr_cidr_entry.configure(state="normal")
            self.cidr_mask_entry.configure(state="disabled")
        else:
            self.cidr_cidr_entry.configure(state="disabled")
            self.cidr_mask_entry.configure(state="normal")
    
    def set_quick_network(self, cidr):
        current = self.vlsm_network_entry.get().split('/')[0]
        self.vlsm_network_entry.delete(0, "end")
        self.vlsm_network_entry.insert(0, f"{current}{cidr}")
    
    def show_message(self, message, msg_type="info"):
        colors = {
            "success": "#38B000",
            "error": "#E71D36",
            "warning": "#FF9500",
            "info": "#4CC9F0"
        }
        
        self.status_message.configure(text=message, text_color=colors.get(msg_type, "white"))
    
    def darken_color(self, hex_color, factor=0.8):
        """Oscurecer un color hexadecimal"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        r = max(0, int(r * factor))
        g = max(0, int(g * factor))
        b = max(0, int(b * factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    @staticmethod
    def ip_to_binary(ip_str):
        octets = ip_str.split('.')
        binary_octets = [format(int(octet), '08b') for octet in octets]
        return '.'.join(binary_octets)
    
    def show_cidr(self):
        self.tabview.set("CIDR")
    
    def show_vlsm(self):
        self.tabview.set("VLSM")
    
    def show_results(self):
        self.tabview.set("Resultados")

        self.calculate_cidr()
        self.calculate_vlsm()
    
    def clear_all(self):
        self.results.clear()
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        for key in self.stats_labels:
            self.stats_labels[key].configure(text="0")
        
        self.show_message(" Todos los resultados limpiados", "success")
    
    def run(self):
        self.window.mainloop()
    
    @staticmethod
    def install_deps():
        import subprocess
        import sys
        
        packages = [
            "customtkinter>=5.2.0",
            "pillow>=10.0.0"
        ]
        
        print(" Instalando dependencias...")
        for package in packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f" {package} instalado")
            except:
                print(f"Error instalando {package}")
        
        print("\n Instalación completada!")

# =========================================================

# ===== EJECUCIÓN PRINCIPAL ========

if __name__ == "__main__":
    # Verificar dependencias
    try:
        import customtkinter
        from PIL import Image
        print(" Dependencias ya instaladas")
    except ImportError:
        CalculadoraIP.install_deps()
        sys.exit(1)
    
    # Ejecutar aplicación
    app = CalculadoraIP()
    app.run()
    
# ==================================== 