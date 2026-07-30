# Course-wise Prod Sequences — Slot-Encoded

*Academic Planning · NRI Institute of Technology · Productised sequence layer · v1 — Python & WAD 1 (remaining courses follow)*

The canonical per-course execution order, verbatim from the SME prod sequences (version `NRI_NIAT_2026`), re-tagged in the productised vocabulary: every row is one **slot** (1 hour); units without a slot number ride the slot above them. Week bands come from the 5+1 weekly plan — **week 1 is the onboarding week (Induction + Dev Tools), so course sequences run wks 2–8 at ~11–12 slots/wk**. The [Day-by-Day](09-nri-day-by-day.md) page places these same slots onto days.

**Stats:** PY 79 slots (40 L · 39 P · 11 MQ · 11 NM units) · WAD 80 slots (43 L · 37 P · 9 MQ · 10 NM units) · wks 2–8, ~11–12/wk · AM/PM block owner

---

## Tagging vocabulary

### Slot types (own a row)
- **L** — **Lecture** (legacy "Session") — video session + its riders in one 1-hour slot.
- **P** — **Practice** — MCQ / coding practice; protected, never converts to Lecture (R14). NxtMock units are a Practice sub-type.

### Unit roles (ride a slot)
- **RM / CS** — Reading Material / Cheat Sheet — self-study riders on the Lecture slot.
- **CQ·A/B** — Classroom Quiz (2 × 5 min) — inside the Lecture slot.
- **MCQ / CP** — MCQ Practice / Coding Practice units inside a Practice slot.
- **MQ-n** — Module Quiz unit — sits at the module-boundary slot in the sequence, but **executes in the Friday assessment block** (R9/R13 policy), not mid-week.
- **NM** — NxtMock unit — **executes as the mock-defend inside SA windows** (retarget policy), not as a standalone slot.

---

## Computer Programming — Python
*PY · 79 slots · AM block owner, wks 2–8*

### Week 2 · PY slots 1–11
| Slot | Type | Lead unit (session / practice) | Riders | Topic |
|---|---|---|---|---|
| 1 | L | Programming with Python (43m) | RM · RM · RM · CQ·A · CQ·B | Introduction to Python |
| 2 | P | MCQ Practice | CP | |
| 3 | L | Coding Practice Walkthrough Part 1 (11m) + Leveraging GenAI for Accelerated Learning (42m) | | |
| 4 | L | Variables and Data Types (27m) | RM · CQ·A · CQ·B | |
| 5 | P | MCQ Practice | CP · **MQ-1** · **NM** | |
| 6 | L | Sequence of Instructions (44m) | RM · CQ·A · CQ·B | Sequence of Instructions |
| 7 | P | MCQ Practice | CP | |
| 8 | L | Input and Output Basics (44m) | RM · CQ·A · CQ·B | |
| 9 | P | MCQ Practice + How to debug your code? (15m) | CP | |
| 10 | L | Type Conversions (49m) | RM · CQ·A · CQ·B | Type Conversions |
| 11 | P | MCQ Practice | CP · **MQ-2** · **NM** | |

### Week 3 · PY slots 12–23
| Slot | Type | Lead unit | Riders | Topic |
|---|---|---|---|---|
| 12 | L | Relational Operators (30m) | RM · CQ·A · CQ·B | Operators |
| 13 | P | MCQ Practice | CP | |
| 14 | L | Logical Operators (41m) | RM · CQ·A · CQ·B | |
| 15 | P | MCQ Practice | CP | |
| 16 | L | Conditional Statements (36m) | RM · CQ·A · CQ·B | Conditional Statements |
| 17 | P | MCQ Practice | CP | |
| 18 | L | Nested Conditional Statements (41m) | RM · CQ·A · CQ·B | |
| 19 | P | MCQ Practice | CP · **MQ-3** · **NM** | |
| 20 | L | Loops (40m) | RM · CQ·A · CQ·B | Loops |
| 21 | P | MCQ Practice | CP | |
| 22 | L | Understanding Coding Question Formats (42m) | | |
| 23 | P | MCQ Practice | | |

### Week 4 · PY slots 24–34
| Slot | Type | Lead unit | Riders | Topic |
|---|---|---|---|---|
| 24 | L | For Loop (34m) | RM · CQ·A | |
| 25 | P | MCQ Practice | CP · CP | |
| 26 | P | Coding Practice - 2 | CP · **MQ-4** · **NM** | |
| 27 | L | String Methods (47m) | RM · RM · CQ·A · CQ·B | Strings Methods |
| 28 | P | MCQ Practice | CP | |
| 29 | L | Nested Loops (36m) | RM · CQ·A · CQ·B | Nested Loops & Loop Control Statements |
| 30 | P | MCQ Practice | CP | |
| 31 | L | Loop Control Statements (59m) | RM · CQ·A · CQ·B | |
| 32 | P | MCQ Practice | CP · **MQ-5** · **NM** | |
| 33 | L | Comparing Strings & Naming Variables (40m) | RM · CQ·A · CQ·B | Comparing Strings & Naming Variables |
| 34 | P | MCQ Practice | CP | |

### Week 5 · PY slots 35–46
| Slot | Type | Lead unit | Riders | Topic |
|---|---|---|---|---|
| 35 | L | Lists (43m) | RM · CQ·A · CQ·B | Lists |
| 36 | P | MCQ Practice | CP · CP | |
| 37 | L | Working with Lists (52m) | RM · CQ·A · CQ·B | |
| 38 | P | MCQ Practice | CP | |
| 39 | L | Lists and Strings (59m) | RM · CQ·A · CQ·B | Lists and Strings |
| 40 | P | MCQ Practice | CP · CP · **MQ-6** · **NM** | |
| 41 | L | Functions (44m) | RM · CQ·A · CQ·B | Functions |
| 42 | P | MCQ Practice | CP | |
| 43 | L | Function Arguments (42m) | RM · CQ·A · CQ·B | |
| 44 | P | MCQ Practice | CP · CP | |
| 45 | L | Built-in Functions (44m) | RM · CQ·A · CQ·B | Built-in Functions |
| 46 | P | MCQ Practice | CP · **MQ-7** · **NM** | |

### Week 6 · PY slots 47–57
| Slot | Type | Lead unit | Riders | Topic |
|---|---|---|---|---|
| 47 | L | List Methods (48m) | RM · CQ·A · CQ·B | List Methods and Tuples |
| 48 | P | MCQ Practice | CP | |
| 49 | L | Tuples & Sequences (46m) | RM · CQ·A · CQ·B | |
| 50 | P | MCQ Practice | CP · CP | |
| 51 | L | Sets (32m) | RM · CQ·A · CQ·B | Sets and Set Operations |
| 52 | P | MCQ Practice | CP | |
| 53 | L | Set Operations (42m) | RM · CQ·A · CQ·B | |
| 54 | P | MCQ Practice | CP · CP · **MQ-8** · **NM** | |
| 55 | L | Dictionaries (30m) | RM · CQ·A · CQ·B | Dictionaries |
| 56 | L | Dictionaries - 2 (20m) | RM · CQ·A · CQ·B | |
| 57 | P | MCQ Practice | CP | |

### Week 7 · PY slots 58–68
| Slot | Type | Lead unit | Riders | Topic |
|---|---|---|---|---|
| 58 | L | Working with Dictionaries (44m) + Working with Dictionaries \| Reading | CQ·A · CQ·B | |
| 59 | P | MCQ Practice | CP · CP | |
| 60 | L | Python Standard Library | RM · CQ·A · CQ·B | Python Standard Library |
| 61 | P | MCQ Practice | CP · CP · **MQ-9** · **NM** | |
| 62 | L | Introduction to Object Oriented Programming (30m) | RM · CQ·A | Object Oriented Programming |
| 63 | P | MCQ Practice | | |
| 64 | L | Object Oriented Programming - Part 2 (41m) | RM · CQ·A · CQ·B | |
| 65 | P | MCQ Practice | CP | |
| 66 | L | Classes & Objects (43m) | RM · CQ·A | Understanding OOPs |
| 67 | P | MCQ Practice | CP | |
| 68 | L | Attributes and Methods (50m) | RM · CQ·A · CQ·B | |

### Week 8 · PY slots 69–79
| Slot | Type | Lead unit | Riders | Topic |
|---|---|---|---|---|
| 69 | P | MCQ Practice | CP · **MQ-8** · **NM** | |
| 70 | L | Encapsulation (46m) | RM · CQ·A | Encapsulation and Inheritance |
| 71 | P | MCQ Practice | CP | |
| 72 | L | Inheritance (50m) | RM · CQ·A | |
| 73 | P | MCQ Practice | CP | |
| 74 | L | Inheritance - Part 2 (47m) | RM · CQ·A · CQ·B | |
| 75 | P | MCQ Practice | CP | |
| 76 | L | Abstraction (47m) | RM · CQ·A | Abstraction and Polymorphism |
| 77 | P | MCQ Practice | CP | |
| 78 | L | Polymorphism (45m) | RM · CQ·A | |
| 79 | P | MCQ Practice | CP · **MQ-9** · **NM** | |

*(Note: MQ-8 and MQ-9 tags recur at slots 54/69 and 61/79 respectively as they appear verbatim in the source SME sequence.)*

---

## Web Application Development 1
*WAD · 80 slots · PM block owner, wks 2–8*

### Week 2 · WAD slots 1–11
| Slot | Type | Lead unit | Riders |
|---|---|---|---|
| 1 | L | Introduction to GenAI in Web Development (30m) | RM |
| 2 | L | Getting Started with Web Development (40m) + Class Room Quiz A + Class Room Quiz B | |
| 3 | P | MCQ Practice | |
| 4 | L | Introduction to HTML (25m) + Class Room Quiz A + Class Room Quiz B | RM |
| 5 | P | MCQ Practice | CP |
| 6 | L | Leveraging GenAI for Accelerated Learning (35m) | RM |
| 7 | L | Introduction to CSS \| Part 1 (40m) + Class Room Quiz A + Class Room Quiz B | RM |
| 8 | P | MCQ Practice | |
| 9 | L | Introduction to CSS \| Part 2 (40m) + Class Room Quiz A + Class Room Quiz B | RM |
| 10 | P | MCQ Practice | CP |
| 11 | L | Introduction to CSS \| Part 3 (43m) + Class Room Quiz A + Class Room Quiz B | RM |

### Week 3 · WAD slots 12–23
| Slot | Type | Lead unit | Riders |
|---|---|---|---|
| 12 | P | Coding Practice | **MQ-1** · **NM** |
| 13 | L | Introduction to CSS Box Model \| Part 1 (35m) + Class Room Quiz A + Class Room Quiz B | RM |
| 14 | P | MCQ Practice | CP |
| 15 | L | Introduction to CSS Box Model \| Part 2 (52m) + Class Room Quiz A + Class Room Quiz B | RM |
| 16 | P | MCQ Practice | CP |
| 17 | L | Coding Platform Walkthrough (7m) | **MQ-2** · **NM** |
| 18 | L | HTML Void Elements & Lists (34m) + Class Room Quiz A + Class Room Quiz B | RM |
| 19 | P | MCQ Practice | CP |
| 20 | P | Foundations of UI/UX Design \| Reading Material | RM |
| 21 | P | Design Process and Inclusive Design \| Reading Material | |
| 22 | L | Website: Behind the Scenes (22m) + Class Room Quiz A + Class Room Quiz B | RM |
| 23 | P | MCQ Practice | |

### Week 4 · WAD slots 24–34
| Slot | Type | Lead unit | Riders |
|---|---|---|---|
| 24 | L | HTML Hyperlinks (37m) + Class Room Quiz A + Class Room Quiz B | RM |
| 25 | P | MCQ Practice | CP |
| 26 | L | Introduction to HTML5 (25m) + Class Room Quiz A + B + C | RM |
| 27 | P | MCQ Practice | CP · **MQ-3** · **NM** |
| 28 | L | HTML Semantic Elements (25m) + Class Room Quiz A + Class Room Quiz B | RM |
| 29 | P | MCQ Practice | CP |
| 30 | L | Leveraging GenAI for Debugging & Building (23m) | RM |
| 31 | L | More CSS Concepts (28m) | RM |
| 32 | P | MCQ Practice | CP |
| 33 | L | CSS Selectors & Inheritance (40m) + Class Room Quiz A + Class Room Quiz B | RM |
| 34 | P | MCQ Practice | **MQ-4** · **NM** |

### Week 5 · WAD slots 35–46
| Slot | Type | Lead unit | Riders |
|---|---|---|---|
| 35 | L | More CSS Selectors (38m) + CSS Selectors \| Learning by Playing + Class Room Quiz A/B/C | RM |
| 36 | P | MCQ Practice | CP |
| 37 | L | CSS Specificity & Cascade (54m) + Class Room Quiz A + Class Room Quiz B | RM |
| 38 | P | MCQ Practice | CP |
| 39 | L | Sizing Elements and Handling Overflow (49m) + Class Room Quiz A + Class Room Quiz B | RM |
| 40 | P | MCQ Practice | CP |
| 41 | L | Box Sizing (15m) + Class Room Quiz A | RM |
| 42 | P | MCQ Practice | **MQ-5** · **NM** |
| 43 | L | Introduction to CSS Flexbox (44m) + Class Room Quiz A + Class Room Quiz B | RM |
| 44 | P | MCQ Practice I | MCQ · CP |
| 45 | L | Introduction to CSS Flexbox \| Part 2 (47m) + Class Room Quiz A | RM |
| 46 | P | MCQ Practice | CP |

### Week 6 · WAD slots 47–58
| Slot | Type | Lead unit | Riders |
|---|---|---|---|
| 47 | L | Introduction to CSS Flexbox \| Part 3 (50m) + Flexbox Froggy Game + Class Room Quiz A + Class Room Quiz B | RM |
| 48 | P | MCQ Practice I | MCQ · CP |
| 49 | L | CSS Media Queries (42m) + Class Room Quiz A + Class Room Quiz B | RM |
| 50 | P | MCQ Practice | CP · CP · **MQ-6** · **NM** |
| 51 | L | Flexbox Sizing (30m) + Class Room Quiz A | RM |
| 52 | P | MCQ Practice | CP |
| 53 | L | Building Responsive Web Page \| Part 1 (40m) | RM · CQ·A · CQ·B |
| 54 | P | MCQ Practice | CP |
| 55 | L | Building Responsive Web Page \| Part 2 (35m) | RM · CQ·A · CQ·B |
| 56 | P | MCQ Practice | CP |
| 57 | L | Building Responsive Web Page \| Part 3 (24m) | RM · CQ·A · CQ·B |
| 58 | P | MCQ Practice | CP · **MQ-7** · **NM** |

### Week 7 · WAD slots 59–69
| Slot | Type | Lead unit | Riders |
|---|---|---|---|
| 59 | L | Building a Website Using VS Code (26m) | RM |
| 60 | L | CSS Grid - 1 (55m) + Class Room Quiz A | |
| 61 | L | CSS Grid - 1 \| Properties + Class Room Quiz B | RM |
| 62 | P | MCQ Practice | CP · **NM** |
| 63 | L | CSS Grid - 2 (46m) + Class Room Quiz A + Class Room Quiz B | RM |
| 64 | P | MCQ Practice | CP |
| 65 | L | CSS Grid - 3 (40m) + Class Room Quiz A + Class Room Quiz B | RM |
| 66 | P | MCQ Practice | CP |
| 67 | L | CSS Grid - 4 (55m) + Class Room Quiz A | |
| 68 | L | CSS Grid - 4 \| Flexbox vs Grid + Class Room Quiz B + CSS Grid \| Learning by Playing | RM |
| 69 | P | MCQ Practice | CP |

### Week 8 · WAD slots 70–80
| Slot | Type | Lead unit | Riders |
|---|---|---|---|
| 70 | L | CSS Positioning \| Part 1 (29m) + Class Room Quiz A + Class Room Quiz B | RM |
| 71 | P | MCQ Practice | CP · **MQ-8** · **NM** |
| 72 | L | CSS Positioning \| Part 2 (24m) + Class Room Quiz A + Class Room Quiz B | RM |
| 73 | P | MCQ Practice | CP |
| 74 | L | Introduction to Tailwind CSS (40m) + Class Room Quiz A + Class Room Quiz B | RM |
| 75 | P | MCQ Practice | CP |
| 76 | L | Introduction to Tailwind CSS \| Part 2 (18m) + Class Room Quiz A | RM |
| 77 | P | MCQ Practice | CP |
| 78 | L | Building Responsive Website using Tailwind CSS (15m) + Class Room Quiz A | RM |
| 79 | P | MCQ Practice | CP |
| 80 | L | Building a Responsive Website using GenAI (30m) | RM · **MQ-9** · **NM** |

---

**Footer:** Source: NRI SME prod sequences (sheet order preserved 1:1 — this page re-tags, never re-orders). Dev Tools (14 built slots) runs inside the week-1 onboarding week — see [Day-by-Day](09-nri-day-by-day.md). Next courses in this format on request: Dev Tools tail, Intro GenAI, Maths, Quant, English Foundation, then Sem-2. Companion: **NRI Day-by-Day** page places these slots onto the 6-day week.
