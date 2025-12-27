# 🛠️ GearGuard - Maintenance Tracker

A complete maintenance management system for **Odoo 18** that connects equipment, maintenance teams, and maintenance requests into one smooth workflow.

---

## ✨ Features

### Equipment Management
- Track assets by department, employee, and category.
- Store serial numbers, purchase dates, and warranty information.
- Assign maintenance teams and default technicians to each equipment.
- Smart button opens all related maintenance requests with a badge count of open items.

### Maintenance Requests
- Support for **Corrective** (breakdown) and **Preventive** (routine) maintenance.
- Auto-fill logic: selecting equipment automatically sets maintenance team and default technician.
- Workflow stages: **New → In Progress → Repaired → Scrap**.
- Duration tracking for hours spent on each repair.
- Validation ensures duration is set before marking a request as repaired.

### Team Management
- Define multiple maintenance teams (e.g., Mechanics, Electricians, IT Support).
- Assign multiple technicians (users) to each team.
- Requests are routed and grouped by team and assigned technician.

### Smart Automation
- Overdue detection: requests with past scheduled dates and not repaired are flagged as overdue.
- Scrap logic: scrapping a request deactivates the related equipment.
- Smart button from equipment form to quickly access all its maintenance history.

### User Interface & Reporting
- **Kanban view**: drag-and-drop cards between workflow stages with overdue visual indicators and technician avatars.
- **Calendar view**: visualize and schedule preventive maintenance on specific dates.
- **List view**: filterable and sortable list with color decoration for overdue requests.
- **Pivot view**: analyze number of requests by team, type, or other dimensions.
- **Graph view**: bar charts for maintenance workload and distribution.
- Search filters and "Group By" options for stage, team, technician, equipment, and request type.

---

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/DarshakBhavsar/The-Ultimate-Maintenance-Tracker.git
   cd The-Ultimate-Maintenance-Tracker
   ```

2. **Copy module to Odoo addons directory**
   ```bash
   cp -r GearGuard /path/to/odoo/addons/
   ```

3. **Restart Odoo server**
   ```bash
   ./odoo-bin -d your_database -u base
   ```

4. **Install the module**
   - Go to **Apps** in Odoo.
   - Clear the "Apps" filter if needed.
   - Search for **GearGuard - Maintenance Tracker**.
   - Click **Install**.

---

## 📖 Quick Start

### 1. Create Equipment
1. Navigate to **Maintenance → Equipment**.
2. Click **New**.
3. Fill in:
   - Name, Serial Number, Category.
   - Department and Employee.
   - Maintenance Team and Default Technician.
4. Save.

### 2. Create Maintenance Request
1. Go to **Maintenance → Maintenance Requests**.
2. Click **New**.
3. Choose **Request Type**: Corrective or Preventive.
4. Select **Equipment** (team and technician will auto-fill).
5. Set **Subject** and **Scheduled Date** (for preventive).
6. Save.

### 3. Use the Workflow
- Start with stage **New**.
- Click **Start Work** to move to **In Progress**.
- Enter **Duration** (hours spent).
- Click **Complete Repair** to move to **Repaired**.
- If equipment is no longer usable, click **Scrap Equipment** to move to **Scrap** and deactivate the equipment.

### 4. Use the Views
- **Kanban**: manage requests visually and drag them between stages.
- **Calendar**: see preventive maintenance scheduled on the right dates.
- **List**: filter and group requests; overdue ones appear highlighted.
- **Pivot/Graph**: analyze requests by team, type, equipment, and more.

---
