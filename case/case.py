import cadquery as cq
from Helpers import show

clearance = 0.2
narrowClearance = clearance / 2
holeClearance = 0.5
relaysPcbNumber = 3
relaysPcbWidth = 32.0
relaysPcbLength = 33.0
relaysPcbThickness = 1.6
relaysPcbHolePositions = ((-5.5, 2.5), (5.5, 2.5))
relaysPcbAudioXPositions = (-11.0, 0, 11.0)
relaysPcbHoleCenterHeight = 2.0
relayPcbToPcbClearance = 1.0
audioHoleCenterHeight = 2.55
audioHoleRadius = 6.0 / 2
proMicroWidth = 18.0
proMicroLength = 33.0
proMicroThickness = 1.6
proMicroUSBHeight = 2.5
proMicroUSBWidth = 7.5
proMicroHolderThickness = 1.0
proMicroHolderLowHeight = 4.0
proMicroHolderCoverLength = 2.6
relaysPcbToUsbClearance = 2.0
wireRadius = 3.0 / 2
mountingHoleHeight = 10.5
mountingHoleRadius = 2.0 / 2
mountSupporerThickness = 1.0
hookWidth = 4.0
hookHeight = 1.5
hookConnectionLength = 1.5
coverMountHoleRadius = 2.8 / 2
coverMountHoleCenterHeight = coverMountHoleRadius * 4
coverMountHoleLength = 10.0
coverMountThickness = 1.0
coverHoleRadius = coverMountHoleRadius + 0.3
boxThickness = 1.5
boxInnerWidth = (relaysPcbWidth + relayPcbToPcbClearance) * relaysPcbNumber \
    - relayPcbToPcbClearance + clearance * 2 \
    + relaysPcbToUsbClearance \
    + proMicroThickness + proMicroUSBHeight \
    + proMicroHolderThickness * 2 + clearance * 2
boxInnerLength = relaysPcbLength + clearance * 2
boxInnerHeight = proMicroWidth + clearance * 2
boxOuterWidth = boxInnerWidth + boxThickness * 2
boxOuterLength = boxInnerLength + boxThickness * 2
boxOuterHeight = boxInnerHeight + boxThickness * 2
wireFixPillowRadius = 3.0 / 2
wireFixPillowHeight = wireRadius * 3
wireFixPillowX = boxInnerWidth - 8.5

cutCover = cq.Workplane('XY') \
    .box(boxInnerWidth, boxInnerLength, boxInnerHeight) \
    .translate((boxInnerWidth / 2, boxInnerLength / 2, boxInnerHeight / 2))
cover = cq.Workplane('XY') \
    .box(boxInnerWidth - narrowClearance * 2,
         boxInnerLength + boxThickness - clearance,
         boxInnerHeight + boxThickness - narrowClearance) \
    .edges('<Y and >Z').fillet(boxThickness) \
    .translate((boxInnerWidth / 2,
                (boxInnerLength - boxThickness - clearance) / 2,
                (boxInnerHeight + boxThickness + narrowClearance) / 2)) \
    .cut(cutCover)

cutBox = cq.Workplane("XY") \
    .box(boxInnerWidth, boxOuterLength, boxOuterHeight)

body = cq.Workplane("XY").box(boxOuterWidth, boxOuterLength, boxOuterHeight) \
    .edges("|X or |Y or |Z").fillet(boxThickness) \
    .cut(cutBox.translate((0, - boxThickness, boxThickness))) \
    .translate((boxInnerWidth / 2,
                boxInnerLength / 2,
                boxInnerHeight / 2))

moutingHoleBase = cq.Workplane("XY").circle(mountingHoleRadius + 1) \
    .extrude(mountingHoleHeight)
moutingHole = cq.Workplane("XY").circle(mountingHoleRadius) \
    .extrude(mountingHoleHeight + boxThickness)
audioHole = cq.Workplane("XZ").circle(audioHoleRadius).extrude(boxThickness)
mountSupporterY = cq.Workplane("XY").box(mountSupporerThickness,
                                         boxInnerLength,
                                         mountingHoleHeight)
mountSupporterXWidth = boxInnerWidth - proMicroThickness - proMicroUSBHeight \
    - clearance * 2 - relaysPcbToUsbClearance
mountSuporterX = cq.Workplane("XY").box(mountSupporterXWidth,
                                        mountSupporerThickness,
                                        mountingHoleHeight)
pcbCenterY = clearance + relaysPcbLength / 2
body = body.union(mountSuporterX.translate((mountSupporterXWidth / 2,
                                            pcbCenterY +
                                            relaysPcbHolePositions[0][1],
                                            mountingHoleHeight / 2)))
hookHoleHeight = hookHeight + holeClearance * 2
hookHole = cq.Workplane("XY") \
    .box(hookWidth + clearance * 2, boxThickness, hookHoleHeight)
hookHoleCenterZ = boxInnerHeight - hookHoleHeight / 2
hookLength = boxThickness + hookConnectionLength + clearance
hook = cq.Workplane('XY').box(hookWidth, hookLength, hookHeight)
hookSupport = cq.Workplane('XY') \
    .box(hookWidth, hookConnectionLength, boxInnerHeight - hookHoleCenterZ)
coverMountHoleBase = cq.Workplane("XZ") \
    .circle(coverMountHoleRadius + coverMountThickness) \
    .extrude(coverMountHoleLength)
coverMountHole = cq.Workplane("XZ").circle(coverMountHoleRadius) \
    .extrude(coverMountHoleLength)
coverHole = cq.Workplane('XZ').circle(coverHoleRadius) \
    .extrude(-boxThickness)

for i in range(0, relaysPcbNumber):
    pcbCenterX = (relaysPcbWidth + relayPcbToPcbClearance) * i \
        + clearance + relaysPcbWidth / 2
    for (x, y) in relaysPcbHolePositions:
        body = body.union(moutingHoleBase.translate((pcbCenterX + x,
                                                     pcbCenterY + y,
                                                     0)))
        body = body.union(mountSupporterY.translate((pcbCenterX + x,
                                                     boxInnerLength / 2,
                                                     mountingHoleHeight / 2)))
        body.cut(moutingHole.translate((pcbCenterX + x,
                                        pcbCenterY + y,
                                        - boxThickness)))
        if (x > 0 and (i == 0 or i == relaysPcbNumber - 1)):
            body.cut(hookHole.translate((pcbCenterX + x,
                                         boxInnerLength + boxThickness / 2,
                                         hookHoleCenterZ)))
            body = body.union(coverMountHoleBase.translate((
                pcbCenterX + x,
                coverMountHoleLength,
                coverMountHoleCenterHeight)))
            body.cut(coverMountHole.translate((
                pcbCenterX + x,
                coverMountHoleLength,
                coverMountHoleCenterHeight)))
            cover.cut(coverHole.translate((
                pcbCenterX + x,
                - boxThickness,
                coverMountHoleCenterHeight)))
            cover = cover.union(hookSupport.translate((
                pcbCenterX + x,
                boxInnerLength - clearance - hookConnectionLength / 2,
                hookHoleCenterZ + hookHeight / 2)))
            cover = cover.union(hook.translate((
                pcbCenterX + x,
                boxInnerLength + boxThickness - hookLength / 2,
                hookHoleCenterZ)))
    for x in relaysPcbAudioXPositions:
        body.cut(audioHole.translate((
            pcbCenterX + x,
            boxInnerLength + boxThickness,
            mountingHoleHeight - audioHoleCenterHeight)))
usbHoleWidth = proMicroUSBHeight + clearance * 2
usbHoleHeight = proMicroUSBWidth + holeClearance * 2
usbHoleBottomZ = (boxInnerHeight - usbHoleHeight) / 2
usbBodyHoleHeight = boxInnerHeight - usbHoleBottomZ + boxThickness
usbHoleCenterX = boxInnerWidth - proMicroThickness - \
    mountSupporerThickness - usbHoleWidth / 2
usbHole = cq.Workplane('XY').box(usbHoleWidth,
                                 boxThickness,
                                 usbBodyHoleHeight)
body.cut(usbHole.translate((
    usbHoleCenterX,
    boxInnerLength + boxThickness / 2,
    usbHoleBottomZ + usbBodyHoleHeight / 2)))

proMicroHolderLowY = cq.Workplane("XY").box(proMicroHolderThickness,
                                            proMicroHolderCoverLength,
                                            proMicroHolderLowHeight)
proMicroHolderHighY = cq.Workplane("XY").box(proMicroHolderThickness,
                                             proMicroHolderCoverLength,
                                             boxInnerHeight)
proMicroHolderXWidth = \
    proMicroThickness + proMicroHolderThickness * 2 + clearance * 2
proMicroHolderX = cq.Workplane("XY") \
    .box(proMicroHolderXWidth, proMicroHolderThickness, boxInnerHeight)
proMicroHolderXCut = cq.Workplane("XY") \
    .box(proMicroHolderXWidth + clearance * 2,
         proMicroHolderThickness + clearance * 2,
         boxInnerHeight + clearance * 2)
proMicroHolderAsOuterX = cq.Workplane('XY') \
    .box(proMicroHolderXWidth, boxThickness, boxInnerHeight)
proMicroHolderAsOuterXCut = cq.Workplane('XY') \
    .box(proMicroHolderXWidth + clearance * 2,
         boxThickness,
         boxInnerHeight + clearance * 2)

proMicroHolderYOuterX = boxInnerWidth - proMicroHolderThickness / 2
proMicroHolderYInnerX = proMicroHolderYOuterX \
    - narrowClearance * 2 - proMicroThickness - proMicroHolderThickness
proMicroHolderYUpperY = boxInnerLength - proMicroHolderCoverLength / 2
proMicroHolderYLowerY = \
    boxInnerLength - proMicroLength - narrowClearance * 2 + \
    proMicroHolderCoverLength / 2

body = body.union(proMicroHolderLowY.translate((
    proMicroHolderYInnerX,
    proMicroHolderYUpperY,
    proMicroHolderLowHeight / 2)))
body = body.union(proMicroHolderHighY.translate((
    proMicroHolderYOuterX,
    proMicroHolderYUpperY,
    boxInnerHeight / 2)))
body = body.union(proMicroHolderHighY.translate((
    proMicroHolderYInnerX,
    proMicroHolderYLowerY,
    boxInnerHeight / 2)))
body = body.union(proMicroHolderHighY.translate((
    proMicroHolderYOuterX,
    proMicroHolderYLowerY,
    boxInnerHeight / 2)))
holderXPosition = (
    boxInnerWidth - proMicroHolderXWidth / 2,
    boxInnerLength - proMicroLength - narrowClearance * 2 -
    proMicroHolderThickness / 2,
    boxInnerHeight / 2)
holderAsOuterXPosition = (
    holderXPosition[0],
    - boxThickness / 2,
    holderXPosition[2])
body = body.union(proMicroHolderX.translate(holderXPosition))
cover.cut(proMicroHolderXCut.translate(holderXPosition))
body = body.union(proMicroHolderAsOuterX.translate(holderAsOuterXPosition))
cover.cut(proMicroHolderAsOuterXCut.translate(holderAsOuterXPosition))

wireHoleWidth = (wireRadius + narrowClearance) * 2
wireHole = cq.Workplane('XY') \
    .box(wireHoleWidth, boxThickness, usbHoleBottomZ) \
    .faces('<Z').edges('|Y').fillet(wireRadius) \
    .translate((proMicroHolderYInnerX - proMicroHolderThickness / 2 -
                wireHoleWidth / 2,
                boxInnerLength + boxThickness / 2,
                usbHoleBottomZ / 2))
body.cut(wireHole)

# body = body.faces('<Z[4]').edges('not(|X or >X)').chamfer(wireRadius / 2)

wireFixPillow = cq.Workplane('XY').circle(wireFixPillowRadius) \
    .extrude(wireFixPillowHeight)
for i in range(0, 3):
    body = body.union(wireFixPillow.translate((
        wireFixPillowX,
        boxInnerLength - wireFixPillowRadius -
        (wireFixPillowRadius + wireRadius) * 2 * i,
        0)))

cover = cover.faces('<Y').edges('not(|X or |Y or |Z)') \
    .chamfer(boxThickness * 0.9)

testZoneWidth = boxOuterWidth * 2 / 3
testZoneLength = boxOuterLength
testZoneHiehgt = boxOuterHeight
testZone = cq.Workplane('XY') \
    .box(testZoneWidth, testZoneLength, testZoneHiehgt) \
    .translate((testZoneWidth / 2 - boxThickness,
                boxInnerLength + boxThickness - testZoneLength / 2,
                boxInnerHeight / 2))
body.cut(testZone)
cover.cut(testZone)

show(body)
show(cover)
