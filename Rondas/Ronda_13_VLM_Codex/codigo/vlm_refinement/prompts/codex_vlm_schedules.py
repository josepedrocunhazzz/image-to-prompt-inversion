from __future__ import annotations

from typing import Any


SCHEDULES: dict[str, list[dict[str, str]]] = {
    "1159_25.png": [
        {
            "prompt": "photorealistic orange juice still life, clear cylindrical glass of pale creamy orange juice, two overlapping orange wheels on the right rim, pale curled citrus peel on the back rim, scattered orange cubes on brown tabletop, round wooden board with cropped orange halves on the left, cropped orange wheel lower right, warm realistic product photo",
            "reason": "Matches the rim garnish, tabletop layout, and cropped fruit positions more closely.",
        },
        {
            "prompt": "clear straight glass of pale orange juice on warm brown table, thin glass rim, two bright orange slices clipped to the right rim, folded pale fruit peel resting behind the rim, small orange chunks scattered in front left, round wood board and orange halves at left edge, realistic soft studio food photo",
            "reason": "Emphasizes the target's glass shape, right-side slices, left board, and front cubes.",
        },
        {
            "prompt": "warm product photo of orange juice, centered clear tumbler filled with smooth pale juice, transparent rim visible, double orange wheel garnish on right, curled yellow orange peel on rear rim, sparse citrus cubes across front left brown tabletop, cropped orange slice at lower right, shallow depth of field",
            "reason": "Reduces clutter while preserving the exact rim and foreground arrangement.",
        },
        {
            "prompt": "realistic orange juice still life on brown wooden surface, tall clear tumbler slightly right of center, creamy orange drink, two overlapping orange rounds on the rim, pale twisted citrus peel on back lip, round wooden coaster left with orange halves, scattered chunky orange pieces in front",
            "reason": "Moves composition toward the target's slightly right-centered glass and left coaster.",
        },
        {
            "prompt": "studio photograph of orange juice in a clear cylindrical glass, smooth pale orange liquid, thin circular rim, pair of orange slices leaning from the right rim, thick curled peel draped over the rear rim, warm brown tabletop, few diced orange pieces foreground left, cropped orange wheel bottom right",
            "reason": "Specifies the target's smooth drink surface and distinctive curled peel.",
        },
        {
            "prompt": "orange juice product photography, transparent tumbler with heavy glass base, pale creamy juice, right rim holding two orange wheels, rear rim holding a pale folded peel strip, brown table with small orange cubes scattered diagonally, round board and cropped orange halves on left, warm shadows",
            "reason": "Targets the heavy glass base, diagonal cube scatter, and warm lighting.",
        },
        {
            "prompt": "close realistic still life, pale orange juice in clear tumbler on matte brown tabletop, two orange slices overlapping at upper right rim, curled candied citrus peel behind the rim, orange cubes spread in lower left foreground, round wooden board at left edge, orange slice cropped lower right",
            "reason": "Uses controlled object placement matching the target frame.",
        },
        {
            "prompt": "warm food photo, single clear orange juice glass, creamy pale orange drink, glass centered slightly right, double orange wheel garnish on right lip, folded yellow peel garnish at back, diced orange fruit pieces on brown surface, left circular wooden board with orange halves, soft realistic shadows",
            "reason": "Keeps the successful still-life terms while tightening target-specific layout.",
        },
        {
            "prompt": "photorealistic citrus drink still life, straight-sided glass of pale orange juice, transparent rim and thick bottom, two fresh orange rounds attached to right rim, curled pale peel strip across rear rim, brown tabletop, scattered orange chunks lower left, cropped orange halves at left edge",
            "reason": "Adds the glass geometry and separates the two garnish types.",
        },
        {
            "prompt": "realistic product photo of orange juice, clear tumbler on warm brown wooden table, smooth pale juice surface, two overlapping orange slices on the right side of the rim, thick curled citrus peel at the back, sparse diced orange pieces in front, round wooden board left",
            "reason": "Prioritizes the largest target features with fewer distracting elements.",
        },
        {
            "prompt": "orange juice still life, cylindrical clear glass with creamy pale orange liquid, thin bright rim, two orange wheels leaning together on right rim, pale twisted peel resting over rear rim, brown tabletop with orange cubes lower left, cropped orange wheel bottom right, warm studio light",
            "reason": "Targets the rim, foreground, and lower-right slice simultaneously.",
        },
        {
            "prompt": "warm realistic food photograph, clear tumbler of pale orange juice, heavy transparent base, double orange slice garnish on right rim, pale curled peel garnish on back rim, matte brown table, small orange chunks scattered from lower left toward glass, round board and orange halves left",
            "reason": "Balances glass detail with the target's object distribution.",
        },
        {
            "prompt": "single glass orange juice still life, pale creamy drink in a straight clear tumbler, two vivid orange cross sections on right rim, folded citrus peel strip at rear, brown tabletop with chunky orange pieces, circular wooden board on left, cropped orange slice at bottom right",
            "reason": "Uses concise concrete cues for cross-section slices and rear peel.",
        },
        {
            "prompt": "photorealistic orange drink scene, clear cylindrical glass slightly right of center, smooth pale orange juice, pair of orange rounds on the right rim, curled pale peel over the back rim, scattered orange cubes on front brown tabletop, left round wooden tray with orange halves",
            "reason": "Stabilizes composition by naming the glass offset and tray position.",
        },
        {
            "prompt": "realistic warm studio still life, orange juice in clear tumbler, thin rim visible above pale liquid, overlapping orange wheels on right edge of glass, curled pale yellow peel garnish behind them, brown wooden surface, diced orange chunks foreground, cropped fruit at left and lower right",
            "reason": "Captures the crop framing around the main glass.",
        },
        {
            "prompt": "orange juice product shot, transparent straight glass with heavy base, creamy orange liquid, two orange slices clipped to the right rim, thick curled citrus peel on rear rim, warm brown table, small fruit cubes lower left, circular wooden board partly visible on left",
            "reason": "A compact variant focused on target geometry and garnish placement.",
        },
        {
            "prompt": "close food photography, pale orange juice glass on brown tabletop, centered clear tumbler, right rim decorated with two overlapping orange cross sections, back rim decorated with folded pale citrus peel, scattered orange cubes in front, round wooden board with oranges on left",
            "reason": "Reiterates the target's three key groups: glass, rim, and left board.",
        },
        {
            "prompt": "warm realistic orange juice still life, clear cylindrical tumbler, smooth pale orange juice, double orange wheel garnish at upper right rim, curled fruit peel draped across back rim, brown wood surface, few diced orange pieces lower left, cropped orange wheel at lower right corner",
            "reason": "Adds corner crop and reduces extra background fruit.",
        },
        {
            "prompt": "studio product photograph, single clear tumbler of creamy orange juice, thin transparent rim, two orange rounds leaning on right rim, pale curled peel garnish behind rim, matte brown tabletop, diagonal scatter of orange chunks in foreground, round wooden board and orange halves left",
            "reason": "Uses the target's diagonal cube scatter and warm product style.",
        },
        {
            "prompt": "photorealistic orange juice still life on brown wooden table, clear straight tumbler slightly right, pale orange drink, two overlapping orange slices on right rim, folded pale citrus peel on rear rim, sparse orange cubes foreground left, cropped orange slices left and bottom right",
            "reason": "Final balanced prompt combining the most stable target descriptors.",
        },
    ],
    "1159_29.png": [
        {
            "prompt": "realistic tropical ocean sunset, tall palm tree trunk rising from shallow turquoise water on the left foreground, large green fronds filling the top, foamy waves around dark rocks at the base, low sun on horizon with bright reflection, distant island mountains on the right, soft clouds",
            "reason": "Adds the target's left palm, foamy surf, sunset reflection, and right mountains.",
        },
        {
            "prompt": "single palm tree at left edge in shallow ocean, textured brown trunk rooted in rocks, broad green fronds overhead, turquoise waves and white foam across foreground, low warm sun centered near horizon, silver reflection on water, hazy island silhouette on right, realistic seascape photo",
            "reason": "Locks the key composition: palm left, sun center, mountains right.",
        },
        {
            "prompt": "photorealistic beach ocean scene, large palm trunk in left foreground surrounded by rocks and surf foam, palm leaves spreading across the upper frame, calm turquoise sea with small waves, sunset glow on horizon, bright water reflection, distant rocky island at right, pale clouds",
            "reason": "Balances the palm scale and target background landmarks.",
        },
        {
            "prompt": "tropical sunset seascape, close palm tree on left rising from shallow water, rough bark trunk, green fronds filling upper left and top center, white foamy surf around the base, turquoise ocean, small sun near horizon, reflective gold path, grey island mountains on right",
            "reason": "Focuses on the large trunk and frond coverage.",
        },
        {
            "prompt": "realistic palm in the sea at sunset, left foreground palm trunk with rocky base, waves breaking around it, sweeping green fronds overhead, blue turquoise ocean under pastel sky, low sun and reflection centered behind waves, distant island ridge on right, soft cloud bands",
            "reason": "Places the sun and reflective water behind the palm base.",
        },
        {
            "prompt": "natural tropical photo, tall coconut palm at left growing from rocks in shallow turquoise ocean, foamy waves in front, full crown of green palm fronds across top, sunset sun low over horizon, bright reflection on rippled water, distant mountain island at right, misty clouds",
            "reason": "Uses coconut palm terms to strengthen the crown and trunk texture.",
        },
        {
            "prompt": "wide square ocean sunset, palm tree trunk cropped on left foreground, dense green fronds canopy overhead, rocks and white foam at trunk base, rolling turquoise waves, warm sun just above horizon, shimmering reflection path, muted island mountains to the right, atmospheric realistic style",
            "reason": "Matches the square crop and high frond canopy.",
        },
        {
            "prompt": "photorealistic tropical coastline, single palm tree dominating left side, bark trunk rising from surf, dark rocks at base, turquoise sea with foamy white waves, low sunset sun near center, glowing water reflection, distant grey island on right horizon, soft blue peach sky",
            "reason": "Strengthens target colors and horizon composition.",
        },
        {
            "prompt": "serene ocean sunset with one palm, left foreground trunk in shallow water, large green fronds filling top half, frothy waves around black rocks, turquoise sea, small sun at horizon, bright silver gold reflection, right side distant island mountains, gentle clouds",
            "reason": "Stabilizes the target's clean single-palm scene.",
        },
        {
            "prompt": "realistic square seascape, large palm tree on left rising from rocky surf, broad feathered fronds across the sky, turquoise waves and foam in foreground, low warm sun over the ocean, reflective light on water, far island cliffs to the right, pale clouds",
            "reason": "Adds feathered frond detail and foreground foam.",
        },
        {
            "prompt": "tropical island sunset photo, palm trunk left foreground with rough segmented bark, crown of green fronds across upper frame, shallow turquoise ocean with white foam, sun low at horizon behind the waves, shiny reflection, distant blue grey mountain island on right",
            "reason": "Highlights trunk bark and mountain tone.",
        },
        {
            "prompt": "single palm tree in shallow turquoise sea, left-side trunk rooted in dark rocks, foamy waves wrapping around base, huge green fronds above, pastel sunset sky, small sun near horizon center, bright reflective water path, distant island landmass on right, realistic photography",
            "reason": "Uses wraparound foam and right landmass cues from the target.",
        },
        {
            "prompt": "ocean sunset scene, tall palm tree on the left with full green canopy, rough bark trunk emerging from rocky shallow water, turquoise waves with white foam, low sun glowing on horizon, reflective wet water in foreground, distant mountains on right, soft atmospheric clouds",
            "reason": "Keeps a balanced photographic description.",
        },
        {
            "prompt": "realistic tropical shore, close palm trunk at left edge, dark rocks and surf foam at its base, sweeping palm leaves covering the upper frame, teal ocean waves, sunset sun near center horizon, shimmering reflection, hazy rocky island at right, pale blue sky",
            "reason": "Moves the trunk to the left edge and keeps top fronds dominant.",
        },
        {
            "prompt": "square tropical ocean photograph, coconut palm rising from shallow surf on left, large green fronds overhead, white foam and wet reflective water foreground, warm low sun on horizon, turquoise sea, soft grey clouds, distant island mountains on the right",
            "reason": "Emphasizes foreground water reflection and right horizon.",
        },
        {
            "prompt": "sunset over turquoise ocean, solitary palm tree at left foreground, rocky base surrounded by white foamy waves, textured bark, full green frond canopy, small sun just above horizon, bright reflection across water, mountain island on right, realistic soft haze",
            "reason": "A concise target-focused variant with all landmarks.",
        },
        {
            "prompt": "photorealistic tropical seascape at golden hour, palm tree trunk in left foreground, fronds arcing across the top, rocks and surf foam below, blue green ocean waves, low sun reflection on water, distant island ridge on right, soft clouds and mist",
            "reason": "Adds golden hour while keeping target geometry.",
        },
        {
            "prompt": "large palm tree in shallow ocean water, left foreground trunk and dark rocks, foamy turquoise waves, green feathered fronds filling top, sunset sun centered low on horizon, reflective path on sea, grey island mountains at right, natural realistic photo",
            "reason": "Reinforces object count and precise placement.",
        },
        {
            "prompt": "realistic beach sunset, single palm on left rising from rocky surf, broad green fronds overhead, turquoise ocean and white foam foreground, small warm sun at horizon, bright reflection, distant right-side island mountains under soft clouds, atmospheric tropical photograph",
            "reason": "Strong final balanced description of the target.",
        },
        {
            "prompt": "tropical ocean sunset photo, close palm tree left with rough trunk and full green crown, rocks and foamy surf at base, turquoise waves across frame, low sun near horizon with shiny water reflection, distant island mountains on right, pale clouded sky",
            "reason": "Final prompt combines scale, water texture, and horizon details.",
        },
    ],
    "1159_3.png": [
        {
            "prompt": "moody anime key art, single blond warrior mage centered, stern face, reflective silver armor and white chest plate, teal ghostly flame mass behind left shoulder, orange flame mass behind right shoulder, glowing curved yellow energy blade crossing the lower body diagonally, dark grey smoky background",
            "reason": "Targets the exact character pose, armor, twin flame masses, and diagonal blade.",
        },
        {
            "prompt": "blond anime fighter in silver futuristic armor, centered waist-up portrait, serious expression, pale chest armor, teal smoke spirit on left, orange fire cloud on right, bright golden curved sword glow sweeping from waist to lower right, dark desaturated painterly background, soft brushwork",
            "reason": "Refines the blade curve and side-color balance.",
        },
        {
            "prompt": "single blond warrior mage, anime concept art, front facing stern gaze, layered silver shoulder armor, white armored torso, cyan green spectral flame behind left side, orange flame swirl behind right side, yellow energy saber arcing across abdomen, dark smoky square crop",
            "reason": "Uses compact subject and symmetric colored flame cues.",
        },
        {
            "prompt": "anime fantasy soldier portrait, blond tousled hair, grey silver armor with rounded shoulders, serious eyes, teal translucent magic plume on left, orange fiery plume on right, glowing amber blade curve across lower chest and waist, dark muted background, painterly soft edges",
            "reason": "Strengthens hair, shoulder armor, and lower energy arc.",
        },
        {
            "prompt": "centered blond anime warrior mage in reflective silver armor, white chest plate, black gloves, stern face, turquoise smoke magic forming a skull-like cloud at left, orange fire magic cloud at right, yellow glowing blade sweeping diagonally across waist, dark grey brush painted key art",
            "reason": "Adds the left spectral shape and right flame mass visible in target.",
        },
        {
            "prompt": "moody anime illustration, single blond armored fighter from thighs up, silver pauldrons, pale armor torso, intense stare, teal ghost flame behind left shoulder, orange flame ring behind right shoulder, luminous golden crescent blade crossing from center waist to lower right, smoky dark background",
            "reason": "Encodes the target's crop and blade endpoint.",
        },
        {
            "prompt": "blond male anime mage warrior, front view, silver sci fi armor, white chest panel, serious expression, soft teal spectral smoke on left side, warm orange fire cloud on right side, bright yellow energy blade at the waist, dark desaturated fantasy concept art",
            "reason": "A cleaner variant focused on core identity and color blocking.",
        },
        {
            "prompt": "anime key visual, stern blond warrior in glossy silver armor, centered portrait, teal magical smoke curling behind left arm, orange flame cloud behind right shoulder, glowing yellow blade arc crossing the torso low, dark charcoal background, soft painterly rendering, square composition",
            "reason": "Tightens the composition and target color placement.",
        },
        {
            "prompt": "single armored anime hero, blond hair, intense face, reflective grey shoulder armor, white torso plates, teal ghostly fire mass left, orange fire mass right, curved golden energy sword slash across lower body, dark smoky background, desaturated brushwork",
            "reason": "Reinforces the single central character and exact slash direction.",
        },
        {
            "prompt": "blond anime warrior mage in silver armor, centered against dark grey mist, serious gaze, pale chest armor and round pauldrons, turquoise magic cloud behind left shoulder, orange flame cloud behind right shoulder, bright yellow curved blade crossing abdomen and extending lower right",
            "reason": "Keeps the target's waist-level blade and color clouds.",
        },
        {
            "prompt": "fantasy anime concept art, single blond armored fighter, front facing half body, polished silver armor, white chest plate, teal spirit flame swirling left, orange flame swirl right, narrow golden energy blade curving across the waist, dark smoky square frame",
            "reason": "Uses half-body framing matching the target.",
        },
        {
            "prompt": "serious blond anime soldier mage, silver futuristic armor, centered torso portrait, teal translucent magic plume on the left, orange fire plume on the right, glowing yellow blade slash along the lower torso, dark muted background, soft brush strokes and smoky edges",
            "reason": "Targets the strongest visible silhouette and color contrast.",
        },
        {
            "prompt": "anime warrior mage portrait, blond messy hair, stern eyes, grey silver armor with white chest, teal ghost smoke behind left shoulder, orange flame vortex behind right shoulder, amber energy sword arc from waist toward lower right corner, moody desaturated painting",
            "reason": "Places the blade toward the lower right corner like the target.",
        },
        {
            "prompt": "single blond armored mage, anime painterly style, centered front pose, reflective silver shoulder plates, pale torso armor, turquoise smoke monster shape on left, orange fire cloud on right, glowing golden curved blade across waist, dark smoky background",
            "reason": "Preserves unusual left smoke shape and right flame shape.",
        },
        {
            "prompt": "moody square anime art, blond warrior in silver armor, stern centered face, teal spectral flame rising at left, orange flame mass rising at right, bright yellow blade curve crossing low across the body, dark grey mist, soft textured brushwork",
            "reason": "A compact target reconstruction with square crop.",
        },
        {
            "prompt": "blond anime warrior mage in reflective silver armor, front-facing stern portrait, white chest plate, black wrist guards, teal magic smoke on left side, orange fire smoke on right side, luminous yellow saber arc across the lower frame, dark fantasy background",
            "reason": "Adds wrist and armor details while keeping the blade low.",
        },
        {
            "prompt": "centered anime fantasy fighter, tousled blond hair, serious eyes, silver armor and pale chest panels, cyan spectral cloud behind left arm, orange flame cloud behind right shoulder, golden energy blade sweeping diagonally across waist, dark smoky painterly scene",
            "reason": "Balances detail and render-friendly phrasing.",
        },
        {
            "prompt": "single blond anime hero in polished grey armor, half body portrait, stern expression, teal ghostly smoke mass at left, orange fire mass at right, bright curved yellow energy blade crossing from center waist to lower right, muted dark brushwork",
            "reason": "Finalizes the most stable target cues in fewer words.",
        },
        {
            "prompt": "anime concept illustration, blond warrior mage centered, reflective silver armor, white torso plate, teal translucent flame behind the left shoulder, orange fiery plume behind the right shoulder, glowing amber blade curve across lower body, smoky charcoal background",
            "reason": "Keeps all target-defining features while simplifying accessories.",
        },
        {
            "prompt": "moody anime key art of a blond armored mage, stern front-facing face, silver shoulder armor and white chest plate, teal magic smoke left, orange fire smoke right, yellow curved energy blade sweeping across the waist, dark desaturated square crop",
            "reason": "Final balanced target prompt for character, pose, colors, and blade.",
        },
    ],
    "1159_7.png": [
        {
            "prompt": "realistic studio object photo, cube shaped hedgehog made from pale peach wooden blocks, visible 4 by 4 square grid sides with rough vertical grooves, tiny hedgehog face peeking from front top edge, large orange spiky fur quills only on the top surface, warm brown background",
            "reason": "Targets the cube grid, tiny face, and top-only quill mass.",
        },
        {
            "prompt": "small cubical hedgehog sculpture, pale peach block cube body, front and side covered in 4 by 4 wooden cube grid texture, rough carved grooves, tiny dark eyes and nose tucked under orange fur at top front, tall amber quills rising upward, realistic warm studio photo",
            "reason": "Strengthens side grid visibility and face placement.",
        },
        {
            "prompt": "compact cube hedgehog on brown studio surface, pale wooden block sides with square tile grid and vertical ridges, tiny face centered just below the top fur, orange tan spiky quills forming a crown on the flat top, realistic macro object photography",
            "reason": "Keeps the target's front face and spiky crown silhouette.",
        },
        {
            "prompt": "realistic hedgehog cube object, peach beige carved wooden cube body, visible square grid sides, rough stacked block texture, small black eyes and nose on front under fur, dense orange spines only across top, tall central quills, warm brown backdrop",
            "reason": "Uses clear material and placement terms for the hybrid object.",
        },
        {
            "prompt": "studio photo of a cubic hedgehog toy, pale peach wood cube with 4 by 4 block grid on front and right side, tiny animal face peeking out at upper front, thick orange quill fur covering only the top face of the cube, soft brown background",
            "reason": "Specifies toy-like cube layout and top face fur.",
        },
        {
            "prompt": "small hedgehog with perfect cube body, pale wooden square tiles on all visible sides, rough fuzzy carved edges, face hidden low in the orange top fur, tiny eyes and nose at front center, long amber spikes upward, realistic studio object photo",
            "reason": "Improves cube regularity and face scale.",
        },
        {
            "prompt": "macro realistic object photo, cubical hedgehog block, peach wooden 4 by 4 grid sides, vertical grooves and fuzzy texture, tiny hedgehog face emerging from front top seam, orange spiky fur cap covering the top only, centered on brown background",
            "reason": "Adds the front top seam where the face appears in the target.",
        },
        {
            "prompt": "cute cube hedgehog sculpture, pale peach beige block cube body, front face made of square wooden columns, right side grid visible, small dark eyes and nose under fluffy orange quills, tall radial spikes on top, warm realistic studio lighting",
            "reason": "Balances cuteness with target material and perspective.",
        },
        {
            "prompt": "realistic square crop, small hedgehog cube, pale wooden block grid body with carved rough grooves, tiny face centered at front top, amber orange quill fur rising from the top surface, body sides clean cubical, matte brown studio background",
            "reason": "A concise target-driven variant for shape and texture.",
        },
        {
            "prompt": "hedgehog shaped like a cube of pale peach wooden blocks, visible 4 by 4 grid on front, side grid wrapping around right face, tiny muzzle and eyes peeking beneath orange quills, spiky fur crown only on top, warm brown realistic product photo",
            "reason": "Targets wraparound grid and tiny muzzle.",
        },
        {
            "prompt": "small cubical hedgehog object, pale wood block sides with stacked square grid texture, rough soft carved ridges, tiny dark face at upper front center, large orange spiky fur tuft covering flat top, centered realistic studio photograph on brown background",
            "reason": "Keeps the top tuft dominant and cube sides visible.",
        },
        {
            "prompt": "realistic studio macro photo, cube body hedgehog, peach beige wooden 4x4 grid sides, chunky square columns, tiny nose and eyes barely visible at front edge, orange amber quills standing tall from top surface, soft shadows on brown backdrop",
            "reason": "Uses 4x4 shorthand and chunky square columns.",
        },
        {
            "prompt": "wooden block hedgehog cube, pale peach cubical body with rough square tile grid, side faces visible, small hedgehog face tucked under top fur, orange tan spikes forming a dense crown on top, centered warm object photography",
            "reason": "Simplifies while preserving all key target features.",
        },
        {
            "prompt": "small hedgehog emerging from a peach wooden cube, square block grid sides, rough vertical grooves, tiny face at front top center, orange spiky quill fur spreading across only the top plane, realistic warm brown studio photo",
            "reason": "Describes the hybrid as hedgehog emerging from cube.",
        },
        {
            "prompt": "cube shaped hedgehog, pale beige wooden block body, visible front and right square grid, fuzzy carved surface, tiny black eyes and pointed nose under orange fur, tall triangular amber quills on top, soft warm studio lighting",
            "reason": "Adds triangular quill silhouette and visible side faces.",
        },
        {
            "prompt": "realistic object photo of a cubical hedgehog, pale peach wood cube with 4 by 4 grid sides, rough stacked block texture, tiny face peeking forward from the top edge, orange spiky quill cap rising upward, plain brown background",
            "reason": "A stable reconstruction of target subject and background.",
        },
        {
            "prompt": "small blocky hedgehog sculpture, perfect cube body in pale peach wood, square grid sides with deep grooves, tiny face centered under orange quills, dense amber spines only on top, warm matte brown studio setting, shallow depth of field",
            "reason": "Adds deep grooves and shallow depth like the target render.",
        },
        {
            "prompt": "macro studio photograph, cubical hedgehog with pale wooden block sides, 4 by 4 front grid and right side grid, rough carved texture, tiny hedgehog face hidden below orange top fur, tall spiky amber quills, centered square composition",
            "reason": "Finalizes grid count, face position, and square composition.",
        },
        {
            "prompt": "cute realistic cube hedgehog, peach beige wooden cube body, rough square block grid on visible sides, tiny eyes and nose at front top seam, orange tan quill fur forming a spiky crown across the top, warm brown background",
            "reason": "Compact target-oriented prompt with seam and crown cues.",
        },
        {
            "prompt": "realistic warm studio object photo, small hedgehog with cubical pale wooden block body, front and side 4 by 4 grid texture, tiny face peeking from upper front, dense orange spiky quills only on the flat top, centered brown backdrop",
            "reason": "Final balanced prompt for the cube hedgehog category.",
        },
    ],
    "7836.png": [
        {
            "prompt": "dark cinematic space painting, tiny astronaut standing at bottom center on curved rocky planet surface, huge pink tan planet band sweeping diagonally across the upper sky, blue black star field and nebula clouds, bright horizon glow behind the planet edge, high contrast cosmic scene",
            "reason": "Targets the tiny astronaut, diagonal planet band, and dark star field.",
        },
        {
            "prompt": "small lone astronaut at bottom center, standing on curved alien ground with long shadow, enormous sloping pink beige planet or ring crossing the top half diagonally, deep black blue space full of stars and cyan nebula wisps, glowing sunrise at horizon, realistic digital painting",
            "reason": "Adds the target's scale contrast and horizon glow.",
        },
        {
            "prompt": "epic space landscape, tiny space explorer near lower center, dark curved planetary surface foreground, massive reddish tan planet limb sweeping from lower left to upper right across sky, blue nebula and star field around it, bright rim light behind horizon, cinematic matte painting",
            "reason": "Places the giant planet limb in the target diagonal.",
        },
        {
            "prompt": "cosmic digital art, astronaut silhouette at bottom center on rocky curved moon, huge pink white dust stripe planet arc dominating upper sky, dark blue black galaxy background with scattered stars, cyan nebula streaks, soft bright glow along the horizon, high contrast",
            "reason": "Uses dust stripe and galaxy cues from the target.",
        },
        {
            "prompt": "tiny astronaut viewed from behind on a curved planet surface, enormous diagonal peach planet band overhead, black starry space, blue nebula clouds on left and right, glowing sunrise along the planetary rim, dark moody high contrast science fiction painting",
            "reason": "Corrects viewpoint and central figure placement.",
        },
        {
            "prompt": "space explorer at bottom center, small figure in white suit, standing on dark rocky horizon, huge slanted dusty pink planet filling the upper frame, black blue star field, luminous blue nebula patches, bright peach glow at the planet edge, cinematic concept art",
            "reason": "Strengthens the astronaut suit and upper planet scale.",
        },
        {
            "prompt": "wide square cosmic scene, tiny astronaut on lower curved foreground planet, large diagonal rose beige planet limb across the sky, black star background with cyan nebula streaks, subtle crater texture on the planet, bright horizon light, moody realistic digital painting",
            "reason": "Adds crater texture and square framing.",
        },
        {
            "prompt": "dramatic alien planet vista, lone astronaut centered near bottom edge, curved ground beneath boots, massive pink tan planet ring or limb sloping across upper sky, dark blue star field, turquoise nebula clouds, glowing rim light at horizon, high contrast",
            "reason": "Keeps the figure low and planet diagonal dominant.",
        },
        {
            "prompt": "science fiction matte painting, small astronaut silhouette at bottom center, dark curved planetary surface, giant dusty rose planet arc crossing the sky diagonally, dense black star field, blue nebula haze, bright sunrise glow behind the arc, cinematic scale",
            "reason": "A compact version emphasizing scale and glow.",
        },
        {
            "prompt": "lonely astronaut on alien world, tiny figure at lower center, curved grey rocky ground, enormous diagonal salmon colored planet band overhead, deep space background with stars and blue nebula, bright light emerging at horizon, dark cinematic digital painting",
            "reason": "Uses the target's salmon band and dark mood.",
        },
        {
            "prompt": "cosmic landscape, small astronaut facing away at bottom, standing on curved planet surface, huge pink beige planet limb stretching diagonally across top, starry black blue sky, cyan galaxy clouds, glowing peach horizon line, realistic high contrast illustration",
            "reason": "Targets the exact viewing direction and horizon line.",
        },
        {
            "prompt": "epic space vista, tiny space suit figure lower center, broad curved foreground world, giant sloped dusty planet across upper frame, dark star field with blue nebula streaks, faint crater lines on planet surface, bright rim glow near center horizon",
            "reason": "Adds faint surface lines from the target planet.",
        },
        {
            "prompt": "dark blue black universe, lone astronaut standing at the bottom edge, curved rocky planetary surface, massive diagonal rose tan planet arc overhead, bright glow behind its lower edge, scattered stars and cyan nebulas, cinematic sci fi painting",
            "reason": "Keeps all target elements with stronger contrast.",
        },
        {
            "prompt": "small astronaut at lower center on a curved alien horizon, huge pale pink planetary band slanting upward across the sky, black star field, blue teal nebula clouds, soft sunrise flare at the center horizon, moody realistic space art",
            "reason": "Improves the center flare and color palette.",
        },
        {
            "prompt": "cinematic space illustration, tiny astronaut in lower foreground, dark curved planet underfoot, enormous dusty peach planet limb sweeping diagonally through upper frame, bright light on horizon, blue nebula wisps and stars in deep black sky, high contrast",
            "reason": "A balanced prompt for subject scale and composition.",
        },
        {
            "prompt": "astronaut alone on a dark planetary ridge, figure small at bottom center, huge diagonal pink beige planet overhead, star-filled black blue sky, cyan nebula streaks, glowing horizon rim behind the figure, realistic moody digital painting",
            "reason": "Adds the glow directly behind the small figure.",
        },
        {
            "prompt": "square sci fi matte painting, tiny astronaut standing in silhouette on curved foreground planet, massive rose colored planet arc across the top, dark blue galaxy background, bright peach rim light at horizon, scattered stars and luminous cyan clouds",
            "reason": "Matches square crop and dark-to-bright hierarchy.",
        },
        {
            "prompt": "deep space scene, lone astronaut lower center, curved rocky terrain, enormous sloping dusty pink planet surface overhead with subtle textures, black star field, blue nebula clouds, bright sunrise glow where the planet meets the horizon, cinematic scale",
            "reason": "Emphasizes target texture and horizon alignment.",
        },
        {
            "prompt": "tiny space explorer on curved alien ground at bottom center, giant peach pink planet band cutting diagonally across upper sky, starry black blue cosmos, turquoise nebula wisps, bright rim glow along horizon, dark high contrast digital painting",
            "reason": "Final compact prompt for the strongest visual match.",
        },
        {
            "prompt": "moody cosmic landscape, small astronaut facing a huge diagonal rose beige planet in the sky, curved dark planet surface at bottom, bright horizon glow, deep blue black star field, cyan nebula streaks, realistic cinematic digital painting",
            "reason": "Final balanced target description with figure, planet, and sky.",
        },
    ],
    "9338.png": [
        {
            "prompt": "vertical storybook illustration, cute colorful dragon hamster centered, orange furry face, big glossy black eye, cream belly, teal blue curled belly scales, rainbow scale quills and horns along the back, tiny clawed paws, swirling yellow orange green flame aura behind, soft painterly brushwork",
            "reason": "Targets the creature's face, belly, rainbow quills, paws, and flame aura.",
        },
        {
            "prompt": "colorful dragon hamster portrait, single central creature sitting upright, orange face with whiskers, large black eye, cream chest fur, teal spiral dragon belly, rainbow scales and spikes down the side, small pink horns, tiny claws, warm yellow green aura flames, painterly fantasy art",
            "reason": "Adds the target's curled belly and upright sitting pose.",
        },
        {
            "prompt": "cute hamster dragon hybrid, centered vertical illustration, peach orange head and snout, glossy black eye, cream fluffy belly, turquoise curled scale patch on chest, rainbow spines and scales on back, little clawed hands and feet, swirling multicolor flame background, soft brush strokes",
            "reason": "Stabilizes the hybrid identity and colorful side scales.",
        },
        {
            "prompt": "storybook fantasy creature, small dragon hamster sitting upright, orange furry face, cream belly, teal blue curled belly scales, pink horns and rainbow dorsal spikes, tiny white claws, big dark eye, yellow orange green magical flame aura around it, painterly vertical portrait",
            "reason": "Matches the vertical central portrait and aura shape.",
        },
        {
            "prompt": "single colorful dragon hamster, cute orange face in left profile, black glossy eye, whiskers, cream chest and belly, curled turquoise dragon scale belly, rainbow bead-like scales on body, pink horns and spines, small clawed paws, smoky multicolor flame aura, soft fantasy painting",
            "reason": "Adds left-profile face and bead-like scale texture.",
        },
        {
            "prompt": "painterly vertical fantasy art, hamster with dragon scales, centered sitting pose, orange head, cream belly fur, teal curled belly plate, rainbow quills and horns along the back, tiny arms with claws, glowing yellow and green flame ribbons behind, dark muted background",
            "reason": "Uses the target's flame ribbons and muted background.",
        },
        {
            "prompt": "adorable dragon hamster illustration, single central creature, orange fur head with whiskers, big black eye, cream fluffy torso, turquoise spiral scale patch, rainbow scales and spikes on shoulders and tail side, small clawed feet, orange yellow green aura flames, soft brushwork",
            "reason": "Keeps the creature cute while adding target-specific scale patches.",
        },
        {
            "prompt": "colorful chubby dragon hamster, upright centered, orange face and ears, cream white belly, blue green curled dragon belly, rainbow scales along side and back, pink horns, tiny clawed paws, large glossy eye, swirling warm flame aura with green light, painterly storybook style",
            "reason": "Emphasizes chubby body, ears, and color aura.",
        },
        {
            "prompt": "fantasy storybook portrait, small hamster dragon hybrid sitting in three quarter profile, orange snout, black shiny eye, cream belly fur, teal curled scales on belly, rainbow dorsal spines, tiny claws, yellow orange green smoky flames rising behind, textured brush strokes",
            "reason": "Targets pose and layered background flames.",
        },
        {
            "prompt": "cute dragon hamster with orange furry head, cream belly, teal blue curled scale chest, rainbow scale spines behind the back, tiny pink horns, small white claws, glossy black eye, centered vertical painterly illustration with swirling golden green flame aura",
            "reason": "A concise reconstruction of the target creature.",
        },
        {
            "prompt": "single central colorful dragon hamster, sitting upright, orange face in profile with whiskers, large black eye, cream fluffy belly, turquoise spiral belly scales, rainbow textured scales across side, pink spines and horns, tiny claws, soft multicolor fire aura background",
            "reason": "Strengthens profile, whiskers, and textured scales.",
        },
        {
            "prompt": "vertical fantasy creature painting, chubby hamster dragon, orange head and ears, cream belly, blue green curled scale patch, rainbow quills down back, small claws and paws, glossy black eye, yellow orange flame ribbons with green glow behind, dark painterly backdrop",
            "reason": "Targets the aura ribbons and central chubby silhouette.",
        },
        {
            "prompt": "adorable hamster dragon portrait, centered sitting creature, peach orange face, cream chest, teal curled belly scales, rainbow bead scales and spikes on back, small pink horns, tiny clawed hands, black glossy eye, colorful smoky flame aura, soft storybook brushwork",
            "reason": "Adds bead-scale texture visible on the body.",
        },
        {
            "prompt": "colorful dragon hamster, vertical storybook illustration, single cute creature with orange face, cream belly, teal blue spiral scale belly, rainbow spines and scales along back, tiny claws, large black eye, swirling yellow green orange magical fire around it",
            "reason": "Balances all target elements with render-friendly wording.",
        },
        {
            "prompt": "cute fantasy dragon hamster sitting upright, orange fur head and snout, whiskers, glossy eye, cream white belly, turquoise curled scales on torso, rainbow dorsal quills and side scales, pink horns, tiny clawed paws, soft smoky multicolor flame aura",
            "reason": "Adds whiskers and torso scale placement.",
        },
        {
            "prompt": "storybook painterly dragon hamster, centered, orange face turned left, big black eye, cream belly fur, teal blue curled dragon belly, rainbow spikes and scales on back and flank, tiny claws, warm yellow orange green aura flames filling the background",
            "reason": "Matches the left-facing head and full aura background.",
        },
        {
            "prompt": "small colorful dragon hamster hybrid, chubby sitting pose, orange furry face, cream belly, blue green spiral scales on chest, rainbow quills behind neck and back, tiny white claws, black glossy eye, swirling golden flame aura and green glow, soft brushwork",
            "reason": "Uses compact anatomy and aura description.",
        },
        {
            "prompt": "vertical fantasy illustration, adorable orange hamster dragon, cream fluffy belly, teal curled belly plate, rainbow scale spines along the back, small pink horns, tiny clawed paws, glossy black eye, smoky yellow orange green fire aura, painterly textured background",
            "reason": "A stable final-style prompt centered on target features.",
        },
        {
            "prompt": "cute colorful dragon hamster centered in a vertical storybook painting, orange face with whiskers, large black eye, cream belly, teal spiral belly scales, rainbow quills and scales, tiny clawed paws, pink horns, swirling yellow green orange flame aura",
            "reason": "Final concise prompt with the target's full creature identity.",
        },
        {
            "prompt": "single central dragon hamster, orange furry face, cream belly, teal curled dragon scales on torso, rainbow spines and scales across back, small pink horns, tiny claws, glossy black eye, soft painterly vertical portrait, swirling golden green orange magical aura",
            "reason": "Final balanced target prompt for subject, color, and aura.",
        },
    ],
}


VISUAL_NOTES: dict[str, dict[str, list[str] | str]] = {
    "1159_25.png": {
        "visual_differences": [
            "The target has a clear orange juice glass with two right-rim orange wheels and a pale curled peel on the rear rim.",
            "The target includes a left wooden board, sparse orange cubes in the foreground, and cropped orange fruit at the frame edges.",
        ],
        "terms_to_keep": ["orange juice still life", "brown tabletop", "realistic product photo"],
        "terms_to_change": ["rim garnish", "fruit placement", "glass shape"],
        "strategy": "Refine garnish placement and tabletop object layout while preserving the warm product photo style.",
    },
    "1159_29.png": {
        "visual_differences": [
            "The target has one large palm tree on the left foreground with fronds filling the top.",
            "The ocean contains turquoise waves, foamy rocks, a low sunset reflection, and distant mountains at right.",
        ],
        "terms_to_keep": ["single palm tree", "turquoise ocean", "low sun reflection", "tropical photo"],
        "terms_to_change": ["palm scale", "rocky surf base", "right horizon island"],
        "strategy": "Keep the single palm and sunset while forcing the left foreground scale and right-side island.",
    },
    "1159_3.png": {
        "visual_differences": [
            "The target is a centered blond armored anime mage with a low curved yellow blade.",
            "The target has teal magic smoke on the left and orange fire smoke on the right over a dark background.",
        ],
        "terms_to_keep": ["blond anime warrior mage", "silver armor", "yellow energy blade"],
        "terms_to_change": ["blade curve and position", "left teal smoke", "right orange fire cloud"],
        "strategy": "Preserve the central character while tightening side magic colors and the waist-level blade arc.",
    },
    "1159_7.png": {
        "visual_differences": [
            "The target is a cube-bodied hedgehog with visible pale wooden block grid sides.",
            "The face is tiny at the front top seam and the orange quills cover only the top surface.",
        ],
        "terms_to_keep": ["small hedgehog", "cubical wooden block body", "orange spiky fur", "realistic studio object photo"],
        "terms_to_change": ["grid side visibility", "tiny face position", "top-only quills"],
        "strategy": "Maintain the cube hedgehog concept while making the wooden grid and face placement explicit.",
    },
    "7836.png": {
        "visual_differences": [
            "The target has a tiny astronaut at the bottom center on a curved dark planet surface.",
            "A huge pink beige planetary band crosses the upper sky diagonally amid blue nebula and stars.",
        ],
        "terms_to_keep": ["small space explorer", "dark cosmic background", "high contrast digital painting"],
        "terms_to_change": ["astronaut placement", "giant diagonal planet band", "horizon glow"],
        "strategy": "Increase the scale contrast between the tiny figure and the enormous diagonal planet.",
    },
    "9338.png": {
        "visual_differences": [
            "The target is a single cute dragon hamster with orange face, cream belly, and teal curled belly scales.",
            "Rainbow spines, tiny claws, and yellow green orange aura flames surround the central creature.",
        ],
        "terms_to_keep": ["colorful dragon hamster", "orange face", "teal belly", "vertical storybook illustration"],
        "terms_to_change": ["rainbow spines", "tiny claws", "flame aura shape"],
        "strategy": "Keep the cute central creature and specify the target's belly scales, quills, claws, and aura.",
    },
}


def schedule_response(
    *,
    target_name: str,
    current_prompt: str,
    iteration: int,
    variants_per_call: int,
) -> dict[str, Any]:
    schedule = SCHEDULES[target_name]
    notes = VISUAL_NOTES[target_name]
    start = max(0, iteration - 1)
    prompts = []
    for offset in range(variants_per_call):
        item = schedule[(start + offset) % len(schedule)]
        prompts.append({"prompt": item["prompt"], "reason": item["reason"]})
    return {
        "visual_differences": notes["visual_differences"],
        "terms_to_keep": notes["terms_to_keep"],
        "terms_to_change": notes["terms_to_change"],
        "strategy": f"{notes['strategy']} Controlled schedule step {iteration} based on current prompt: {current_prompt[:140]}",
        "prompts": prompts,
    }
