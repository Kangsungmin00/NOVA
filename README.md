# NOVA-SIM

> A spatial simulation engine for persistent virtual worlds, autonomous agents, and digital twins.

**NOVA-SIM**은 공간 안에 존재하는 객체들이 상태와 규칙을 가지고 시간에 따라 변화하는 **공간 기반 시뮬레이션 프로젝트**입니다.

단순히 사전에 정의된 이벤트를 재생하는 것이 아니라, World와 Entity의 상태 변화가 누적되면서 시뮬레이션 결과가 생성되는 구조를 목표로 합니다.

장기적으로는 도시, 모빌리티, 물류, 보행자·군중 시뮬레이션, 로보틱스 및 디지털 트윈과 연결할 수 있는 범용적인 공간 시뮬레이션 기반을 구축하는 것을 지향합니다.

> NOVA-SIM은 현재 초기 아키텍처를 구축하고 검증하는 단계입니다.

---

## Project Direction

NOVA-SIM은 다음 흐름을 중심으로 발전시킵니다.

```text
World
  ↓
Time
  ↓
Entity
  ↓
Behavior
  ↓
State Transition
  ↓
Event
  ↓
State History
  ↓
Simulation Result
  ↓
Analysis
```

핵심은 공간 객체를 화면에 표현하는 것 자체가 아니라, **시간에 따른 상태 변화를 구조화된 데이터로 관리하고 관측할 수 있는 Simulation Engine**을 만드는 것입니다.

향후 실제 공간 데이터와 연결하여 다양한 Domain Simulation으로 확장할 수 있는 구조를 목표로 합니다.

---

## Architecture

현재 구현된 NOVA-SIM의 기본 데이터 흐름은 다음과 같습니다.

```text
Scenario
    ↓
  World
    ↓
Entity / Simulation Time
    ↓
get_state()
    ↓
World State
    ↓
Observer / API
```

공간 객체 시각화는 다음 흐름으로 구성됩니다.

```text
Entity State
    ↓
Renderer
    ↓
Leaflet
    ↓
World View
```

각 계층의 책임을 가능한 한 분리하여 Simulation Logic이 특정 UI나 표현 방식에 종속되지 않도록 개발하고 있습니다.

---

## Implemented

### Simulation World

Simulation의 최상위 상태를 관리하는 `World`를 구현했습니다.

현재 World는 다음 상태를 관리합니다.

```text
World ID
Simulation Time
Tick
Random Seed
World Center
Entities
```

World 상태는 외부에서 직접 내부 속성을 조회하는 대신 다음 인터페이스를 통해 제공합니다.

```python
state = world.get_state()
```

---

### Simulation Time

실제 시스템 시간과 분리된 Simulation Time을 구현했습니다.

현재 `World.step()` 호출 시:

```text
tick + 1
simulation time + 1 minute
```

의 상태 변화가 발생합니다.

이를 기반으로 향후 Entity와 환경의 상태 변화를 Tick 단위로 처리할 수 있도록 확장합니다.

---

### Spatial Entity

World 내부에 존재하는 공간 객체의 최소 모델인 `SpatialEntity`를 구현했습니다.

현재 Entity는 다음 상태를 가집니다.

```text
entity_id
entity_type
latitude
longitude
```

Entity는 World에 등록되어 World State의 일부로 관리됩니다.

```text
World
└─ Entities
   ├─ Entity
   ├─ Entity
   └─ ...
```

---

### Scenario

Simulation의 초기 조건을 UI 및 Simulation Core와 분리하기 위해 Scenario 계층을 구성했습니다.

현재 Scenario는 다음과 같은 초기 상태를 정의합니다.

```text
World ID
Start Time
Random Seed
World Center
Initial Entities
```

Observer에서는 World를 직접 구성하지 않고 Scenario를 통해 생성된 World를 사용합니다.

---

### Observer

Simulation 상태를 직접 관측할 수 있도록 **NiceGUI 기반 NOVA Observer**를 구현했습니다.

현재 Observer는 다음 네 영역으로 구성됩니다.

```text
┌─────────────────────────────────────┐
│ SIMULATION CONTROL                  │
├──────────────────────┬──────────────┤
│                      │              │
│ WORLD VIEW           │ INSPECTOR    │
│                      │              │
├──────────────────────┴──────────────┤
│ EVENT LOG                           │
└─────────────────────────────────────┘
```

현재 Observer에서 확인할 수 있는 주요 상태는 다음과 같습니다.

```text
World ID
Simulation Time
Tick
Random Seed
Spatial Entity
```

`STEP`을 실행하면 World 상태가 변경되고 Observer에 반영됩니다.

```text
STEP
  ↓
World.step()
  ↓
World.get_state()
  ↓
Observer Update
```

---

### Spatial Visualization

Observer의 World View에 Leaflet 기반 지도를 연결했습니다.

지도 중심 위치는 Observer에 직접 정의하지 않고 World State의 `world_center`를 사용합니다.

```text
Scenario
   ↓
World Center
   ↓
World State
   ↓
Observer
   ↓
Leaflet
```

따라서 Scenario에 따라 다른 공간을 사용하더라도 Observer의 지도 코드 자체를 변경하지 않는 구조를 유지합니다.

---

### Entity Renderer

Entity의 상태와 화면 표현을 분리하기 위해 Renderer 계층을 구현했습니다.

현재 Entity Type에 따라 다른 지도 표현을 적용할 수 있습니다.

```text
agent      → 📍
vehicle    → 🚚
robot      → 🤖
warehouse  → 🏭
```

Observer는 특정 Entity의 표현 방식을 직접 결정하지 않고 Renderer에 전달합니다.

이를 기반으로 향후 Point뿐 아니라 Line, Polygon, Route, Grid 등 다양한 공간 표현으로 확장할 수 있습니다.

---

### World API

World 상태를 외부 시스템에서 조회할 수 있도록 FastAPI 기반 최소 API를 구현했습니다.

현재 제공되는 Endpoint는 다음과 같습니다.

```text
GET  /api/world
POST /api/world/step
```

이를 통해 다음 데이터 흐름을 검증했습니다.

```text
World
  ↓
get_state()
  ↓
FastAPI
  ↓
HTTP / JSON
```

---

## Project Structure

현재 주요 프로젝트 구조는 다음과 같습니다.

```text
NOVA/
│
├─ README.md
├─ pyproject.toml
├─ uv.lock
├─ .python-version
│
├─ docs/
│  ├─ 00_project_overview.md
│  └─ devlog/
│
├─ src/
│  └─ nova_sim/
│     ├─ __init__.py
│     ├─ world.py
│     ├─ entity.py
│     ├─ scenario.py
│     ├─ renderer.py
│     ├─ observer.py
│     └─ api.py
│
└─ tests/
```

각 모듈의 현재 책임은 다음과 같습니다.

| Module        | Responsibility                |
| ------------- | ----------------------------- |
| `world.py`    | World 상태 및 Simulation Time 관리 |
| `entity.py`   | 공간 객체의 기본 데이터 모델              |
| `scenario.py` | Simulation 초기 조건 구성           |
| `renderer.py` | Entity 상태의 공간 시각화             |
| `observer.py` | Simulation 상태 관측 UI           |
| `api.py`      | World 상태 외부 API               |

---

## Development Environment

현재 NOVA-SIM은 다음 기술을 사용합니다.

```text
Python
uv
NiceGUI
Leaflet
FastAPI
Git / GitHub
```

Python 프로젝트 및 의존성은 `uv`를 사용하여 관리합니다.

---

## Development Principles

### Small First

처음부터 현실 전체를 구현하지 않고 검증 가능한 최소 단위부터 확장합니다.

### Reproducibility

동일한 초기 조건과 Random Seed에서 가능한 한 동일한 Simulation Result를 재현할 수 있는 구조를 지향합니다.

### Separation of Concerns

Simulation, Scenario, Visualization, API, Storage의 책임을 분리합니다.

```text
Simulation
≠
Visualization
≠
Persistence
```

### Observable Simulation

Simulation 내부의 상태 변화는 가능한 한 외부에서 관측할 수 있도록 설계합니다.

```text
Simulation Code
      ↓
State
      ↓
Observer
```

### Data as a Result

Simulation 결과를 화면 표현에만 사용하지 않고 향후 분석 가능한 데이터로 저장할 수 있는 구조를 지향합니다.

---

## Documentation

세부 설계, 기술 결정 및 개발 과정은 `docs/`에서 관리합니다.

```text
docs/
├─ project overview
├─ world model
├─ architecture
├─ decisions
└─ devlog
```

README에는 프로젝트의 큰 방향과 **실제로 구현 및 검증된 주요 기능만 기록**합니다.

세부 구현 과정, 문제 해결 과정, 실험 및 향후 단기 작업은 Devlog와 별도 설계 문서에서 관리합니다.

---

## Status

**Early Development — Core Architecture & Observability**

현재 NOVA-SIM은 다음 기반을 구축한 상태입니다.

```text
World
  ↓
Simulation Time
  ↓
Spatial Entity
  ↓
Scenario
  ↓
State Interface
  ↓
Observer
  ↓
Spatial Visualization
  ↓
External API
```

이 기반 위에서 공간 객체의 상태 변화와 행동을 점진적으로 확장해 나갈 예정입니다.
