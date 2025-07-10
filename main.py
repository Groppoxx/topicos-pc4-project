import asyncio
from multiprocessing import Process, set_start_method, Manager
from agentes.avion_agent import AvionAgent
from agentes.torre_agent import TorreControlAgent
from visual.visualizador import iniciar_visualizacion
from shared_state import set_estado_agentes

def run_simulacion(estado_agentes):
    set_estado_agentes(estado_agentes)

    async def iniciar_agentes():
        torre = TorreControlAgent("torre@localhost", "1234")
        await torre.start(auto_register=False)

        for i in range(3):
            jid = f"avion{i}@localhost"
            avion = AvionAgent(jid, "1234")
            await avion.start(auto_register=False)
            await asyncio.sleep(1)

        print("[MAIN] Todos los agentes iniciados.")
        while True:
            await asyncio.sleep(10)

    asyncio.run(iniciar_agentes())

if __name__ == "__main__":
    set_start_method("spawn")

    manager = Manager()
    estado_agentes = manager.dict()

    for i in range(3):
        estado_agentes[f"avion{i}@localhost"] = "Volando"

    visual = Process(target=iniciar_visualizacion, args=(estado_agentes,))
    visual.start()

    run_simulacion(estado_agentes)
