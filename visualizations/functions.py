def wheelEvent(self, event):
    '''zoom in/out on wheel event'''
    delta_y = event.angleDelta().y()
    factor = self.zoom_factor if delta_y > 0 else 1 / self.zoom_factor
    self.view.scale(factor, factor)

def regenarate_clicked(self):
    '''generate a new layout if the current choice is "random"'''
    if self.choice_combo.currentText() == "random":
        self.set_nx_layout("random")
        
def toggle_timer(self):
    '''toggles timer based on the QCheckBox run_checkbox'''
    if self.run_checkbox.isChecked():
        self.timer.start(abs(self.slider.value()))
    else:
        self.timer.stop()

def update_timer_interval(self):
    '''update the timer slider interval'''
    new_interval = self.slider.value()
    self.timer.setInterval(abs(new_interval))
    
def update_slider_label(self):
    '''updates slider level (seconds per tick)'''
    self.slider_label.setText(f"{abs(self.slider.value() / 1000)} seconds per tick")

def reset(self):
    '''reset button pressed'''
    while self.change_stack:
        self.undo_change()

def undo_change(self):
    '''undo button pressed'''
    if self.change_stack:
        previous_node_item, previous_state = self.change_stack.pop(0)
        previous_node_item.values = previous_state
        previous_node_item.color = previous_state['color']

        _, next_state = self.change_stack.pop(0)
        self.network.node_values_change.insert(0, next_state)

        previous_node_item.update()
              
def change_node_color(self, times):
    '''accessed only when button is clicked, gets first value from the list'''
    for _ in range(times):
        if self.network.node_values_change:
            values_change_dict = self.network.node_values_change.pop(0)
            node_name = None
            for key, value in values_change_dict.items():
                if key == 'id':
                    node_name = value
                    break
            self.update_node_color(node_name, values_change_dict)
            
def update_node_color(self, node_name, values_change_dict):
    '''updates node values, called from 'change_node_color' '''
    node_item = self.nodes_map[str(node_name)]
    previous_state = node_item.values.copy()
    for key, value in values_change_dict.items():
        node_item.values[key] = value
    node_item.color = node_item.values['color']
    next_state = node_item.values.copy()
    self.change_stack.insert(0, (node_item, previous_state))
    self.change_stack.insert(1, (node_item, next_state))
    node_item.update()