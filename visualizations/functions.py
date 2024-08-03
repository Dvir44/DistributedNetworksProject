# zoom in/out on wheel event
def wheelEvent(self, event):
    delta_y = event.angleDelta().y()
    factor = self.zoom_factor if delta_y > 0 else 1 / self.zoom_factor
    self.view.scale(factor, factor)

# generate a new layout if the current choice is "random"
def regenarate_clicked(self):
    if self.choice_combo.currentText() == "random":
        self.set_nx_layout("random")
        
# toggles timer based on the QCheckBox run_checkbox
def toggle_timer(self):
    if self.run_checkbox.isChecked():
        self.timer.start(abs(self.slider.value()))
    else:
        self.timer.stop()

# update the timer slider interval
def update_timer_interval(self):
    new_interval = self.slider.value()
    self.timer.setInterval(abs(new_interval))
    
# updates slider level (seconds per tick)
def update_slider_label(self):
    self.slider_label.setText(f"{abs(self.slider.value() / 1000)} seconds per tick")

# reset button pressed
def reset(self):
    while self.change_stack:
        self.undo_change()

# undo button pressed
def undo_change(self):
    if self.change_stack:
        previous_node_item, previous_state = self.change_stack.pop(0)
        previous_node_item.values = previous_state
        previous_node_item.color = previous_state['color']

        _, next_state = self.change_stack.pop(0)
        self.network.node_values_change.insert(0, next_state)

        previous_node_item.update()
              
# accessed only when button is clicked, gets first value from the list     
def change_node_color(self, times):
    for _ in range(times):
        if self.network.node_values_change:
            values_change_dict = self.network.node_values_change.pop(0)
            node_name = None
            for key, value in values_change_dict.items():
                if key == 'id':
                    node_name = value
                    break
            self.update_node_color(node_name, values_change_dict)
            
#pdates node values, called from 'change_node_color'
def update_node_color(self, node_name, values_change_dict):
    node_item = self.nodes_map[str(node_name)]
    previous_state = node_item.values.copy()
    for key, value in values_change_dict.items():
        node_item.values[key] = value
    node_item.color = node_item.values['color']
    next_state = node_item.values.copy()
    self.change_stack.insert(0, (node_item, previous_state))
    self.change_stack.insert(1, (node_item, next_state))
    node_item.update()