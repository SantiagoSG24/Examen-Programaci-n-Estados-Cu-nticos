import sys
from repositorio import RepositorioDeEstados
from operador_cuantico import crear_operador_x, crear_operador_h, crear_operador_z

def mostrar_menu():
    print("\n--- Simulador Cuántico ---")
    print("1. Listar estados cuánticos")
    print("2. Agregar nuevo estado")
    print("3. Aplicar operador cuántico")
    print("4. Medir estado cuántico")
    print("5. Guardar estados a archivo")
    print("6. Cargar estados desde archivo")
    print("0. Salir")

def main():
    repo = RepositorioDeEstados()
    
    # Operadores predefinidos
    operadores = {
        "X": crear_operador_x(),
        "H": crear_operador_h(),
        "Z": crear_operador_z()
    }
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        try:
            if opcion == "1":
                print("\nEstados cuánticos registrados:")
                estados = repo.listar_estados()
                if not estados:
                    print("No hay estados registrados")
                else:
                    for estado in estados:
                        print(estado)
                        
            elif opcion == "2":
                print("\nAgregar nuevo estado cuántico")
                id = input("ID del estado: ")
                vector_str = input("Vector de estado (ej. '1 0' para [1, 0] o '0.707 0.707'): ")
                base = input("Base (deje vacío para 'computacional'): ") or "computacional"
                
                # Convertir el string del vector a lista de complejos
                componentes = vector_str.split()
                vector = []
                for comp in componentes:
                    try:
                        # Intentar convertir a complejo (permite "1", "0.5", "1+2j", etc.)
                        num = complex(comp)
                        vector.append(num)
                    except ValueError:
                        raise ValueError(f"Componente inválida: '{comp}'")
                
                repo.agregar_estado(id, vector, base)
                print(f"Estado {id} agregado exitosamente")
                
            elif opcion == "3":
                print("\nAplicar operador cuántico")
                print("Operadores disponibles:", ", ".join(operadores.keys()))
                
                id_estado = input("ID del estado a transformar: ")
                nombre_op = input("Nombre del operador: ").upper()
                
                if nombre_op not in operadores:
                    print(f"Error: Operador '{nombre_op}' no disponible")
                    continue
                
                operador = operadores[nombre_op]
                nuevo_id = input("ID para el nuevo estado (deje vacío para auto-generar): ") or None
                
                nuevo_estado = repo.aplicar_operador(id_estado, operador, nuevo_id)
                print(f"Operador aplicado. Nuevo estado creado:")
                print(nuevo_estado)
                
            elif opcion == "4":
                print("\nMedir estado cuántico")
                id_estado = input("ID del estado a medir: ")
                
                probs = repo.medir_estado(id_estado)
                print(f"\nProbabilidades de medición para {id_estado}:")
                for estado_base, prob in probs.items():
                    print(f"- Estado base {estado_base}: {prob*100:.2f}%")
                    
            elif opcion == "5":
                archivo = input("Nombre del archivo para guardar (ej. estados.json): ")
                repo.guardar(archivo)
                print(f"Estados guardados en {archivo}")
                
            elif opcion == "6":
                archivo = input("Nombre del archivo para cargar (ej. estados.json): ")
                repo.cargar(archivo)
                print(f"Estados cargados desde {archivo}")
                
            elif opcion == "0":
                print("Saliendo del programa...")
                sys.exit(0)
                
            else:
                print("Opción no válida. Intente nuevamente.")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()