[33mcommit 7878ffacaa955993cdc513740c5028566eca2b4e[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mfeature/code[m[33m)[m
Author: enoc <225378395+enocpari69@users.noreply.github.com>
Date:   Thu Apr 16 18:13:01 2026 -0400

    Agregar opciones de cancelar y confirmar en todas las funciones de gestión
    
    - Agregar funciones auxiliares: input_con_cancelar(), confirmar_accion(), obtener_opcion_menu()
    - Modificar agregar_pacientes/actualizar_paciente/eliminar_paciente con cancelar + resumen + confirmar
    - Modificar agregar_dentista/actualizar_dentista/eliminar_dentista con cancelar + resumen + confirmar
    - Modificar agregar_cita con cancelar en cada paso + resumen + confirmar
    - Modificar agregar_horario_atencion con cancelar + confirmar
    - Modificar eliminar_cita con mostrar datos y confirmación mejorada
    - Modificar obtener_hora_12h() para soportar cancelación con '0'

[33mcommit b81d5a68de4ae25c2a473187eaeb80da4d342cc5[m
Author: enoc <225378395+enocpari69@users.noreply.github.com>
Date:   Wed Apr 15 23:18:35 2026 -0400

    Actualizar: ignorar archivos .md en git

[33mcommit 311ea8ad3a0efd77733e3748c3b106cca9810cb8[m
Author: enoc <225378395+enocpari69@users.noreply.github.com>
Date:   Wed Apr 15 23:18:31 2026 -0400

    Agregar: AGENTS.md con instrucciones para agentes

[33mcommit 467c401896c6bc91c7aabff7440bdb909ecaf09c[m
Author: enoc <225378395+enocpari69@users.noreply.github.com>
Date:   Wed Apr 15 23:18:24 2026 -0400

    Corregir: eliminar método duplicado tipo() en clase Persona

[33mcommit 4f9224ea6d692e5c2fc75b9f86b177b7be5d017b[m
Author: enoc <225378395+enocpari69@users.noreply.github.com>
Date:   Wed Apr 15 22:51:11 2026 -0400

    agregue  services
    /horarios_services.py
    /citas_services.py
    /dentista_services.py
    /pacientes_services.py
    "seguimiento de servicios inicio"

[33mcommit 9a5d848b2f530faa2c9fa7fd783b6e41d7f670fb[m
Author: enoc <225378395+enocpari69@users.noreply.github.com>
Date:   Wed Apr 15 22:33:04 2026 -0400

    agregando cita.py

[33mcommit 1c842c2ec0b862f37c5ee3d5f899d8c6316f0b72[m
Author: enoc <225378395+enocpari69@users.noreply.github.com>
Date:   Sun Apr 12 20:12:26 2026 -0400

    agregando horarios de atencion
    horario_atencion.py

[33mcommit c39a21437bb54f42609a2672fd8b55743f8542d1[m
Author: enoc <225378395+enocpari69@users.noreply.github.com>
Date:   Sun Apr 12 12:41:40 2026 -0400

    agregado pacientes.py  clase paciente
    clase hija de persona

[33mcommit 833e5552ec5256f6049049b9f54fb41b85028e31[m
Author: enoc <225378395+enocpari69@users.noreply.github.com>
Date:   Sun Apr 12 12:39:51 2026 -0400

    Agregar .gitignore para Python

[33mcommit 7aac6176e31ab241b5734a715f1bd14a4fadbbaa[m
Author: enoc <225378395+enocpari69@users.noreply.github.com>
Date:   Sun Apr 12 12:26:38 2026 -0400

    agregando dentista.py a los cambios a confirmar
    dentista.py clase dentista clase hija de persona,
     con atributos adicionales como especialidad

[33mcommit 9533173bb04f9027f4e4a4330a0cd31f0e82737a[m
Author: enoc <225378395+enocpari69@users.noreply.github.com>
Date:   Sun Apr 12 12:17:55 2026 -0400

    agregando cambios a persona.py
    molde clase padre para las clases dentista y paciente

[33mcommit d02a15a75c64a93245d9d48dd937210c3da75042[m[33m ([m[1;32mmaster[m[33m, [m[1;32mfeature/codechat[m[33m)[m
Author: enoc <225378395+enocpari69@users.noreply.github.com>
Date:   Sun Apr 5 14:12:05 2026 -0400

    archivo persona .py se encuentra la clase persona, la cual es la clase padre de paciente y dentista, por lo que se modifico para agregar el atributo id, el cual es necesario para poder identificar a cada persona de manera unica, ademas se modifico el constructor para que reciba el id como parametro y se asigna al atributo id de la clase persona.

[33mcommit 108b03c171111f199328c54704c285a844916d80[m
Author: enoc <225378395+enocpari69@users.noreply.github.com>
Date:   Tue Mar 31 21:28:54 2026 -0400

    initial commit
