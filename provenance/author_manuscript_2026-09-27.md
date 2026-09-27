THE SERIOUS SCIENCE OF SMALL ANNOYANCES

# **The Science of Why Onions Make Us Cry**

### From the chemistry inside a damaged cell to the physics of the air between the cutting board and your eyes.

![Peeling Onions, by Lilly Martin Spencer, ca. 1852, the Memorial Art Gallery, Rochester, NY, acquired in June, 1988 (source).](https://miro.medium.com/v2/eb88c6c27bfb7e7ab3e76c953a87ee177d152d47b9fb4c71074ff5a54f3b615a "image.png")
As if by magic, an onion can interrupt the preparation of a meal without ever touching your face. It remains on the cutting board beneath the knife, yet after a few cuts your eyes begin to sting and tears blur the next slice. Advice arrives from almost everyone who has cooked. Chill the onion, sharpen the knife, leave the root intact, put water nearby, or hold something in your mouth. A hacker might even suggest Tor Browser, though its onions will be of little use here.

Advice about cutting onions has passed among cooks across cuisines and generations, and the remedies can sound like competing answers to the same question, even though they address different stages of the path from onion to eye. Blade sharpness changes how the tissue is damaged; cooling may alter its chemistry and mechanics; moving air changes where released material travels; and well-sealed eye protection can restrict access to the eyes. To assess this advice, we need to follow the irritant through those stages and ask what each experiment or calculation actually establishes.

## What the knife sets in motion

Damage to onion tissue allows the enzyme alliinase to act on a sulfur-containing precursor called isoalliin. An enzyme is a biological catalyst, a molecule that accelerates a reaction. Here its action produces an unstable intermediate, 1-propenesulfenic acid, from which another enzyme, lachrymatory-factor synthase, produces the volatile compound syn-propanethial S-oxide, also called the onion lachrymatory factor. “Lachrymatory” means tear-inducing.\[1\]

![image.png](https://miro.medium.com/v2/7a42002d46e616554168af8edec4e59ecc3c913406defd7c56051b75e74b3c21 "image.png")
_Figure 1: Crystal structure of Lachrymatory Factor Synthase from Allium cepa. \[1\]_

The second enzyme is central to this pathway. In 2002, Shinsuke Imai and colleagues showed that the lachrymatory factor is formed through its action, revising the earlier explanation that it formed spontaneously after alliinase had acted.\[2\] The sequence identifies the irritant and shows why damage to the tissue matters. Saying that onions contain sulfur explains neither which compound is produced nor how it forms.

![figure_01_chemistry.png](https://miro.medium.com/v2/ab70212281e758f32bc0cafaddf73321d096a747dc4fedab6c5551c3d917bddd "figure_01_chemistry.png")
_Figure 1. A schematic of the verified reaction sequence and the subsequent route to irritation.\[1\], \[2\] Enzyme names identify catalysts above the corresponding steps. Coproducts and competing reactions are omitted; the diagram is not an atom-balanced reaction or a drawing of cellular dimensions._

The pathway can also be changed experimentally. Colin Eady and colleagues suppressed expression of the synthase gene in onions and measured substantially less lachrymatory factor, alongside changes in other sulfur compounds.\[3\] Their experiment connects that enzyme to formation of the irritant while showing that reducing it can also change the sulfur chemistry associated with flavour. The result does not, by itself, tell us how the onion will taste.

![image.png](https://miro.medium.com/v2/cf6d8189a3f816af343b54dadc83dad3ea3eab03eb2160ab9cd6b06839342539 "image.png")
_Figure 3: The main sulfur pathway following tissue disruption in onion. \[3\]_

## When the irritant reaches the eye

The compound’s effect on the eye has been tested with synthesized onion lachrymatory factor. In a study of 91 healthy volunteers, Hisayo Higashihara and colleagues exposed one eye to the compound and measured both the time until irritation became intolerable and the increase in the curvature radius of the tear meniscus, the narrow reservoir of tears along the eyelid. Responses varied among age groups.\[4\]

The experiment establishes a physiological response to the identified compound under its exposure conditions, but it does not establish a universal airborne concentration at which every cook begins to cry, or a rule that twice the concentration produces twice the tears. Airborne concentration, the amount reaching an eye, and that eye’s sensory and tear responses are different quantities.

For that reason, the calculations that follow stop at modeled exposure near a specified location. They examine how a specified source reaches that location under specified air motion, but do not predict discomfort or tear volume. The familiar explanation that onion fumes form sulfuric acid in the eyes is not established as the mechanism by the primary evidence cited here.

## A sharp blade changes the release

The cut that initiates the chemical processes also disturbs the tissue mechanically. In controlled guillotine-style experiments, Zixuan Wu and colleagues observed an initial burst of droplets followed by the breakup of liquid strands. Blunter blades and faster cuts produced more droplets and greater droplet energy.\[5\]

These observations support a sharp blade and controlled cuts when the aim is to reduce spray. The investigators measured cutting mechanics and droplets, not airborne lachrymatory-factor concentration or human tears, so their results cannot tell us how much either practice reduces eye irritation. Vapour and droplets may originate in the same cut, but a measurement of one does not establish the amount of the other.

Slower cuts may eject fewer droplets with each stroke while extending the preparation. Whether that reduces exposure over the whole task depends on what is released throughout cutting and where the air carries it.

## The air between the board and your face

Once an irritant has entered the air, its route depends on more than the quantity produced. Air motion carries it, and spreading distributes it over a larger volume. At a fixed location, the concentration can _increase as a plume arrives_ and _fall as that plume passes or disperses_.

The source changes with time too. Mette Marie Løkke and colleagues continuously analysed the headspace above freshly cut onions and found that signals associated with lachrymatory factor and its breakdown products were prominent early as the mixture of volatile compounds evolved.\[6\] Their measurements concern a particular sampling arrangement. We will use them as evidence that release evolves, without treating that apparatus as a direct measurement of concentration beside a cook's face.

We can investigate the transport without pretending to know the emissions of every onion. Let $c(\mathbf x,t)$ denote the gas-phase concentration at position $\mathbf x$ and time $t$, and let $Q(t)$ be the amount entering the air per second. For a prescribed uniform air velocity $\mathbf u$, our model is

$$
\frac{\partial c}{\partial t}+\mathbf u\cdot\nabla c=D_{\mathrm{eff}}\nabla^2c+Q(t)\rho_s(\mathbf x).
$$

The left-hand side describes change at a position and transport by air motion. On the right, $D_{\mathrm{eff}}$ controls diffusion, while $\rho_s$ distributes the source over a small region and integrates to one over space. Thus integrating the source term over space gives exactly $Q(t)$.

Here, the coefficient is an assumed effective mixing coefficient, not a measured molecular diffusivity of onion lachrymatory factor, and we prescribe it to study a controlled transport problem. We also omit chemical loss in the baseline calculation and treat the surrounding space as unbounded. The model contains no cutting board, body, wall, thermal plume, or fan rotor. Its air velocity is an input, not a computed flow around a kitchen.

These idealizations let us isolate the effects of release timing and airflow direction. They make the calculation tractable, but its numerical results are not calibrated predictions of exposure in a particular kitchen.

## Following the same source in four directions

The numerical comparison places the observation point 30 centimetres horizontally and 40 centimetres vertically from the centre of the source, a straight-line distance of 50 centimetres. The source has a Gaussian spatial profile with a coordinate standard deviation of 3 centimetres, and concentration is averaged with a Gaussian observation profile whose coordinate standard deviation is 1 centimetre. These are simply measures of spatial spread in each direction. The averaging is a mathematical probe and it does not model absorption by the eye.

We compare four cases with exactly the same release history. There is either _no mean drift_, a _uniform current directed along the source-to-observer line_, the _opposite current_, or a _current perpendicular to that line_. Each moving case has speed $0.05\,\mathrm{m\,s^{-1}}$, and all use $D_{\mathrm{eff}}=0.003\,\mathrm{m^2\,s^{-1}}$. 

In the “no mean drift” case, we set the average airflow to zero but retain the model’s assumed spreading through mixing. This, however, does not represent perfectly still air in which molecular diffusion would be the only means of transport.

Every instantaneous release spreads as a three-dimensional Gaussian whose centre moves with the air. Contributions from successive release times are also added to obtain the complete concentration history. The displayed images are _slices through that three-dimensional solution_ and not two-dimensional plumes given an arbitrary thickness.

![animation_01_transport.gif](https://miro.medium.com/v2/00deffaaee38357de11fc8f5cdd7bdd46ce88d1dc304db277c63e2d296095ed1 "animation_01_transport.gif")
_Animation 1. A slice at_ $y=0$ _through the calculated three-dimensional concentration field. All panels share one logarithmic scale, source history, and clock; values below the stated display floor are white. The transverse current is perpendicular to the displayed plane, so material can leave the slice while remaining in the three-dimensional field. The marked observation location is in the plane. These are normalized model concentrations, not measured fumes, tracked droplets, or predicted tears. The MP4 and a static frame are included in the accompanying package._

To compare the histories, we define the concentration integrated over an observation period $T$,

$$
E_T=\int_0^T c_e(t)\,dt,
$$

where $c_e(t)$ is concentration at the observation location after the stated spatial averaging. If $c_e$ is measured in moles per cubic metre, $E_T$ has units of mole-seconds per cubic metre. It is an exposure measure, not an absorbed dose.

We divide by the common total emitted amount $M$, so the numerical comparison requires no invented estimate of how many moles an onion releases. The baseline source uses the two-stage release law with time constants of 2 and 4 seconds introduced below. Over the first 120 seconds, it gives the following results.

![table_01_air_motion.png](https://miro.medium.com/v2/ade5944fa6fca96a8d2399087340fb7fc568d89fdd7f381c8905d54f143d8e4b "table_01_air_motion.png")
These differences belong to this specific geometry and these parameters. They are _not_ efficacy estimates for a household fan. Their useful practical implication, however,  is that the _route matters_ particularly: the same emitted amount can give very different exposure at one location, and adding a current does not necessarily lower the exposure there. A current directed from the onion toward the observer can, of course, deliver the plume sooner and produce more exposure within the chosen period.

The observation period matters particularly. With no mean drift, the first 120 seconds account for only about 55% of the exposure the model accumulates over all future time. The remaining 45% builds up later, even though the concentration is then low. Calling the two-minute value “total exposure” would overlook that later contribution.

We can show that an analytic limit explains the directional effect. For an instantaneous point release of amount $M$, a point observer at displacement $\mathbf r$, a constant mixing coefficient $D$, uniform velocity $\mathbf u$, and no chemical loss, the exposure over all time is

$$
E_\infty=\frac{M}{4\pi Dr}\exp\left(\frac{\mathbf u\cdot\mathbf r-|\mathbf u|r}{2D}\right),\qquad r=|\mathbf r|.
$$

Here the dot product $\mathbf u\cdot\mathbf r$ measures the current's alignment with the line to the observer. A current directly toward the point observer makes the exponent zero, while a transverse or opposing current makes it negative.

When the source and observer are treated as points, airflow directed straight toward the observer changes the timing of exposure, but the concentration integrated over all future time remains equal to the no-drift value. Our numerical calculation gives the source a finite Gaussian width and averages concentration around the observer, so the two all-time integrals differ slightly, as the supplement shows.

The formula relates airflow direction, distance, and spreading in a single expression. Its prediction follows from the assumed uniform flow and unbounded space and applying it to a particular kitchen would require checking those assumptions, of course.

## A lower peak can leave a longer exposure

The release history also offers another way to examine a common intuition.

> If a treatment makes the release less intense, does it necessarily reduce the observer’s exposure over all future time?

To isolate this question, we represent production and escape with two successive first-order steps. Let $P$ be the accessible precursor, $L$ the retained irritant, and $k_p$ and $k_e$ their effective rates. The illustrative source obeys

$$
\frac{dP}{dt}=-k_pP,\qquad \frac{dL}{dt}=k_pP-k_eL,\qquad Q=k_eL.
$$

Initially $P=M$ and $L=0$. This construction assigns unit molar yield and no side loss, so all of the initial amount eventually enters the air. It is a deliberately reduced source model and not a fitted reconstruction of onion enzymes, of course. Its two time constants describe the chosen release histories, and they certainly are not laboratory measurements of chilling or knife technique.

We compare one history with time constants of 2 and 4 seconds and another with time constants of 10 and 20 seconds. The second source releases the same amount over a longer period. Both then pass through exactly the same transport model, with air directed toward the observation point.

![figure_02_release_exposure.png](https://miro.medium.com/v2/6f1fdba609547989e61de72d61fb9877b93bedaf556d117bebdec2014e0c543d "figure_02_release_exposure.png")
_Figure 2. Two hypothetical source histories with equal total release, followed by concentration and accumulated exposure at the same observation location, with flow toward it at 0.05 metres per second. The source constants are illustrative. Changes in peak or early exposure are not measured benefits of chilling or slow chopping; integration over all future time gives the same exposure for these equal-yield sources under unchanged transport._

The longer release lowers the peak normalized concentration from $3.61$ to $1.21\,\mathrm{m^{-3}}$. Yet its exposure over the first 120 seconds is $0.992$ times that of the shorter release, and both approach the same exposure when integrated over all future time. A large change in the peak has accompanied only a small change in the two-minute integral.

The equality can be derived without choosing the two time constants. Let $q(t)=Q(t)/M$ be the release rate per unit total emission, so its integral is one, and let $K(a)$ be the concentration response to a unit instantaneous release after elapsed time $a$. Then

$$
\frac{c_e(t)}{M}=\int_0^t q(s)K(t-s)\,ds.
$$

Integrating over all observation times adds the complete contribution of every release. Since both functions are nonnegative, we can change the integration order and obtain

$$
\frac{E_\infty}{M}=\left(\int_0^\infty q(s)\,ds\right)\left(\int_0^\infty K(a)\,da\right)=\int_0^\infty K(a)\,da.
$$

Both release schedules eventually emit the same amount of irritant. A slower release can lower and delay the concentration peak, and it can change exposure during the first two minutes. Does that lower peak mean less exposure in total?

> No. When the same amount is emitted and airflow and spreading remain unchanged, this model gives the same concentration integrated at a fixed observation point over all future time for both schedules.

A cook does not remain at that point indefinitely. They finish and step away; the onion may be covered or removed, and the airflow may change. These changes can alter exposure during preparation. If a remedy reduces the total amount emitted, the model’s all-time integral also falls, provided transport remains unchanged. To judge a remedy, we need to consider the whole task: a low concentration at one moment does not establish lower exposure over that period.

## Which practices have support?

Our calculation ends with concentration near the cook’s face. The irritant must still reach the eyes, so well-sealed goggles have a clear purpose, however spectacular they may look at the cutting board:

> they restrict access around the eyes, while ordinary spectacles leave gaps.

The argument is physical rather than a measured percentage reduction from a controlled onion-cutting trial—and the protection depends, of course, on the fit and seal.

Before the irritant reaches the face, however, moving air can change its route. A current that carries material away from the cook has the right geometry; one that carries it from the board toward the eyes could make matters worse. Our calculation shows why direction matters, but cannot tell us how well a particular fan or extractor works. Even if we set turbulence aside, an extractor’s rated airflow cannot tell us how much irritant it captures from a particular cutting board. The path from the onion to the inlet still matters.

A wet towel beside the board is sometimes proposed as another way to intercept what the air carries. For that to work, enough irritant would have to reach the towel before reaching the eyes and be taken up quickly enough. Water in direct contact with the cut onion may instead change what is released at the surface. Neither effect, however, follows from the mere presence of water nearby, and we found no controlled comparison establishing that a nearby wet towel prevents tears.

At the cut itself, however, the knife has a measurable mechanical effect. Wu and colleagues found that blunter blades and faster cuts produced more droplets and greater droplet energy.\[5\] Their results support a sharp blade and controlled cuts for reducing spray, but they do not measure the effect on airborne lachrymatory factor or tears. Slower cutting can also keep the cook at the board longer, so less spray per cut need not mean less exposure over the whole task.

Chilling may change both the onion’s chemistry and the way its tissue breaks under a blade. In Wu and colleagues’ comparison, onions refrigerated at 1 °C for 12 hours ejected visibly more liquid, while the droplet-speed distributions showed no significant difference.\[5\] Yet the observation concerns spray and does not establish whether chilling increases or decreases tearing, or how long an onion should be refrigerated to prevent it.

The onion itself can differ before the first cut too. Kato and colleagues produced mutant lines that formed substantially less lachrymatory factor after tissue disruption and had reduced alliinase activity. Their sensory panel assessed fresh bulb tissue by chewing it, rather than by performing a standardized chopping task.\[7\] These results show that induced mutation followed by selection can reduce an onion’s production of the irritant. Nonetheless, they do not make “sweet” or “mild” a guarantee that an onion will leave a cook’s eyes dry.

![figure_03_remedies.png](https://miro.medium.com/v2/cb99d08f6f4763ce189493bf61fc8f44fe1a4ce257e7c12215e259e9276fbde7 "figure_03_remedies.png")
_Figure 3. A practical assessment of the outcomes supported by the reviewed literature and by physical reasoning. Mechanistic recommendations are distinguished from direct intervention measurements. "Not established" describes the reviewed evidence and does not prove that an intervention never helps. Knife and cultivar findings concern the endpoints specified in references \[5\] and \[7\]._

For leaving the root intact, holding bread or a spoon in the mouth, and lighting a candle, our targeted search did not locate adequate peer-reviewed evidence of reduced onion-induced tearing.

Chewing gum needs separate attention because a patent describes a small test involving onion grating. It reports that the average time before tears began was longer with a menthol-containing gum than with a control gum without the cooling agent.\[8\] That comparison concerns the added ingredient, however, and not whether chewing ordinary gum protects the eyes. The patent reports averages without showing how much the results varied between participants, and we found no independent confirmation in the literature reviewed.

A sharp blade and controlled cuts have experimental support for reducing spray. To reduce what reaches the eyes, the physical reasoning favours airflow that carries released material away from the face and goggles that seal around the eyes. Chilling remains less certain because the evidence reviewed does not establish its effect on tearing over a complete preparation task.

The common experience begins at the cut, but whether it ends in tears depends on what is produced, how it leaves the tissue, where the air carries it, and how the eyes respond.

---

## References

1. Silvaroli, J. A., Pleshinger, M. J., Banerjee, S., Kiser, P. D., and Golczak, M. (2017). "Enzyme That Makes You Cry--Crystal Structure of Lachrymatory Factor Synthase from Allium cepa." _ACS Chemical Biology_, 12(9), 2296-2304. [DOI](https://doi.org/10.1021/acschembio.7b00336).
2. Imai, S., Tsuge, N., Tomotake, M., et al. (2002). "An onion enzyme that makes the eyes water." _Nature_, 419, 685. [DOI](https://doi.org/10.1038/419685a).
3. Eady, C. C., Kamoi, T., Kato, M., et al. (2008). "Silencing Onion Lachrymatory Factor Synthase Causes a Significant Change in the Sulfur Secondary Metabolite Profile." _Plant Physiology_, 147(4), 2096-2106. [DOI](https://doi.org/10.1104/pp.108.123273).
4. Higashihara, H., Yokoi, N., Aoyagi, M., Tsuge, N., Imai, S., and Kinoshita, S. (2010). "Using synthesized onion lachrymatory factor to measure age-related decreases in reflex-tear secretion and ocular-surface sensation." _Japanese Journal of Ophthalmology_, 54, 215-220. [DOI](https://doi.org/10.1007/s10384-009-0786-0).
5. Wu, Z., Hooshanginejad, A., Wang, W., Hui, C.-Y., and Jung, S. (2025). "Droplet outbursts from onion cutting." _Proceedings of the National Academy of Sciences_, 122(42), e2512779122. [DOI](https://doi.org/10.1073/pnas.2512779122). [Original investigators' data and code](https://osf.io/5xady/).
6. Løkke, M. M., Edelenbos, M., Larsen, E., and Feilberg, A. (2012). "Investigation of Volatiles Emitted from Freshly Cut Onions (Allium cepa L.) by Real Time Proton-Transfer Reaction-Mass Spectrometry (PTR-MS)." _Sensors_, 12(12), 16060-16076. [DOI](https://doi.org/10.3390/s121216060).
7. Kato, M., et al. (2016). "Production and characterization of tearless and non-pungent onion." _Scientific Reports_, 6, 23779. [DOI](https://doi.org/10.1038/srep23779).
8. Mirkheshti, N. (2009). "Use of cooling agents for treatment or prevention of lacrimation or eye burning." European patent publication EP2014333A1, published 14 January 2009. [Patent text](https://patents.google.com/patent/EP2014333A1/en). Preliminary patent evidence; not a peer-reviewed clinical study.