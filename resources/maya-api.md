maya python api:

# Translate x, y, z
cmds.setAttr('object.translate', x, y, z)

# Rotate x, y, z
cmds.setAttr('object.rotate', x, y, z)

# Select object
cmds.select('object')

# Set keyframe
cmds.setKeyframe(t='framenumber')
