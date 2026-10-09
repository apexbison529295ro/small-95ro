We need to write a small responsive component library. Requirements:

- single file, under 60 lines
- short module docstring
- standard library only
- include a __main__ block
- code only reply

Goal: small responsive component library. In Python, we can create a simple CLI library that prints responsive components? Or provide a small GUI? Since standard library only, we can use tkinter for a responsive component library. But tkinter may not be considered "component library" but we can create a simple wrapper for components that auto adjust based on window resizing.

We need to keep under 60 lines. Let's try to write something that defines a simple component system: a base Component class, a Label and Button that auto adjust width. In __main__, we create a small window with a responsive frame.

Alternatively, create a command-line library that responds to terminal width.

Given the requirement: small responsive component library. I'd choose Tkinter as the UI library. We'll implement a simple responsive frame that resizes its child components based on window width.

We need to implement a base class Component that accepts parent, and draws itself. For demonstration, implement a Label component and a Button component. On resize, we reposition them.

But we need to do all under 60 lines. Let's try:

- line 1: module docstring
- define Component base class with init
- define LabelComponent subclass
- define ButtonComponent subclass
- define ResponsiveFrame subclass of Frame that manages layout
- __main__ block create Tk root, add components, run mainloop

We need to count lines. Let's write and count.

We need to pick a simple approach: In ResponsiveFrame, we can override 'configure' binding to <Configure> event and reposition children.

Simplify: Just create two elements side-by-side that adjust width of each to half.

Let's write code.

Line 1: docstring.

Line 2: import tkinter as tk

Then define Component.

Add code. Let's draft.

I'll count lines:

1: """Simple responsive component library using tkinter."""
2: import tkinter as tk
3:
4: class Component:
5:     def __init__(self, parent):
6:         self.widget = tk.Frame(parent)
7:
8: class LabelComponent(Component):
9:     def __init__(self, parent, text):
10:        super().__init__(parent)
11:        self.widget = tk.Label(parent, text=text, bg='lightblue')
12:
13: class ButtonComponent(Component):
14:     def __init__(self, parent, text, command=None):
15:         super().__init__(parent)
16:         self.widget = tk.Button(parent, text=text, command=command, bg='lightgreen')
17:
18: class ResponsiveFrame(tk.Frame):
19:     def __init__(self, parent, components):
20:         super().__init__(parent)
21:         self.components = components
22:         for comp in components:
23:             comp.widget.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
24:         self.bind('<Configure>', self.resize)
25:
26:     def resize(self, event):
27:         # Adjust components width proportionally
28:         total = len(self.components)
29:         for comp in self.components:
30:             comp.widget.config(width=event.width // total)
31:
32: if __name__ == '__main__':
33:     root = tk.Tk()
34:     root.title('Responsive Demo')
35:     frame = ResponsiveFrame(root, [
36:         LabelComponent(root, 'Left'),
37:         ButtonComponent(root, 'Right')
38:     ])
39:     frame.pack(fill=tk.BOTH, expand=True)
40:     root.mainloop()

Count lines: Let's count: 1 docstring, 2 import, 3 blank, 4 class, 5 def, 6 widget, 7 blank, 8 class Label, 9 def, 10 super, 11 widget, 12 blank, 13 class Button, 14 def, 15 super, 16 widget, 17 blank, 18 class Responsive, 19 def, 20 super, 21 components, 22 for, 23 widget.pack, 24 bind, 25 blank, 26 def, 27 comment, 28 total, 29 for, 30 config, 31 blank, 32 if main, 33 root, 34 title, 35 frame init, 36 label, 37 button, 38 list close, 39 frame.pack, 40 root.mainloop.

That's 40 lines. Under 60. Good. But we didn't use the component base's widget, we replaced it with specific label/button frame. Actually we set self.widget to Label or Button directly, not using Frame. In Component init, we set widget to Frame, but then overwritten. That's okay.

Potential improvement: For responsive, using pack with expand=True fill=BOTH likely already auto-resizes. But we also adjust width in resize, but width config may not be effective for Label/Buttons? Might set width in characters, not pixels. But it's fine for demo.

We need to ensure we pack components inside ResponsiveFrame: we are passing root to LabelComponent; but then in ResponsiveFrame, we pack component.widget into the ResponsiveFrame itself? Wait: In main, we create components passing root as parent. Then we pass these to ResponsiveFrame, which packs them into self. That means LabelComponent's widget is a Label attached to root, but then we pack it into ResponsiveFrame. That may cause parent mismatch. We should create components with parent=self. But we don't have self at that point. Instead, we can have components created without parent, and then responsive frame sets parent. Simpler: in ResponsiveFrame, we can create new components as part of itself. But for simplicity, we can just create components with parent=self after we create the frame.

Simpler: In main, create frame, then create components passing frame as parent. That requires frame to exist. So in main, create frame, then create components with frame parent, and then add them to frame's components list? We can modify to:

frame = ResponsiveFrame(root, [])
label = LabelComponent(frame, 'Left')
button = ButtonComponent(frame, 'Right')
frame.components.extend([label, button])
for comp in frame.components: comp.widget.pack...

But we need to pack inside frame. Let's change accordingly.

Simplify: Instead of passing components list, we can have ResponsiveFrame create and manage them. But we need to pass component definitions.

Alternative: remove components list approach and just have frame that does pack for its children automatically. But we need to show responsive logic.

Option: In ResponsiveFrame, we pass a list of tuples (component_class, kwargs). Then inside __init__, we create each component with self as parent. That would be nice.

Implement:

class ResponsiveFrame(tk.Frame):
    def __init__(self,parent,components):
        super().__init__(parent)
        self.components=[]
        for cls, kwargs in components:
            comp=cls(self, **kwargs)
            comp.widget.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            self.components.append(comp)
        self.bind('<Configure>', self.resize