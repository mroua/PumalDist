"""

        <div id="editSidebar" style="margin-top: -10px"
             class="fixed right-0 top-0 bottom-0 w-4/5 backprimer shadow-lg transform translate-x-full transition-transform duration-300 z-50">
            <div class="flex justify-between items-center p-4 border-b">
                <h3 class="text-lg font-semibold textslate">Editer une commande</h3>
                <button id="closeEditSidebar" class="text-xl textslate">&times;</button>
            </div>

            <!-- Step 1: Select Products -->
            <div id="editstep1" class="p-4 containerdef flex flex-col">
                <div class="p-4 h-28 flex justify-around border border-gray-300 rounded-lg mb-4 gap-4">
                    <!-- Type Filter -->
                    <div class="mb-4 w-64">
                        <label for="edittypeFilter" class="block text-sm font-medium text-gray-700 mb-2">Type</label>
                        <select id="edittypeFilter"
                                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                            {% for fil in liste_type %}
                                <option value="{{ fil.id }}">{{ fil.designation }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <!-- Measure Filter -->
                    <div class="mb-4 w-64">
                        <label for="editmeasureFilter" class="block text-sm font-medium text-gray-700 mb-2">Mesure</label>
                        <select id="editmeasureFilter"
                                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">

                            {% for fil in liste_mesure %}
                                <option value="{{ fil.id }}">{{ fil.designation }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <!-- Field Filter -->
                    <div class="mb-4 w-64">
                        <label for="editcolorfilter" class="block text-sm font-medium text-gray-700 mb-2">Couleur</label>
                        <select id="editcolorfilter"
                                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">

                            {% for fil in liste_couleur %}
                                <option value="{{ fil.id }}">{{ fil.designation }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <!-- Field Filter -->
                    <div class="mb-4 w-64">
                        <label for="editdistfield" class="block text-sm font-medium text-gray-700 mb-2">Selectionner le
                            distributeur</label>
                        <select id="editdistfield"
                                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                            {% for fil in liste_distributeur %}
                                <option data-designation="{{ fil.designation }}" data-username="{{ fil.user.nom }}"
                                        data-email="{{ fil.user.email }}"
                                        id="{{ fil.id }}" value="{{ fil.id }}">{{ fil.designation }}</option>
                            {% endfor %}
                        </select>
                    </div>


                </div>
                <div class="h-4/6 overflow-y-auto">
                    <div id="editproductList" class="grid gap-4 w-full"></div>
                </div>
                <div class="flex justify-end pb-2">
                    <button id="editgoToStep2" class="editgoToStep2 h-10 bg-blue-500 text-white px-4 py-2 rounded-lg">
                        Suivant
                    </button>
                </div>
            </div>

            <!-- Step 2: Review Selected Products -->
            <div id="editstep2" class="p-4 hidden">
                <h3 class="text-lg font-semibold mb-4">Review Products</h3>
                <div class="h-4/6 overflow-y-auto">
                    <div id="editselectedProducts"></div>
                </div>


                <div class="flex justify-end font-bold">
                    <div class="grid grid-cols-4">
                        <div class="defaultvaldark">Total HT:</div>
                        <div class="text-right col-span-3 defaultvaldark" id="edittotalPrice">0 DA</div>

                        <div class="defaultvaldark">Total TTC:</div>
                        <div class="text-right col-span-3 defaultvaldark" id="edittotalPriceTTC">0 DA</div>
                    </div>
                </div>


                <div class="flex justify-between items-center mt-4">
                    <button id="editgoToStep1" class="bg-gray-500 text-white px-4 py-2 rounded-lg">Retour</button>
                    <button id="editgoToStep3" class="bg-blue-500 text-white px-4 py-2 rounded-lg">Suivant</button>
                </div>
            </div>

            <!-- Step 3: Confirm Order -->
            <div id="editstep3" class="p-4 hidden defaultboldval">
                <!-- Logo Section -->
                <div class="h-4/5 w-full flex flex-col  items-center">

                    <div class="w-2/3">
                        <div class="flex justify-center mb-4">
                            <img src="{% static 'images/puma.svg' %}" alt="Company Logo" class="h-16">
                        </div>

                        <!-- Facture Details -->
                        <div class="grid grid-cols-2 gap-4 mb-4">
                            <!-- Recipient Details -->
                            <div class="">
                                <p id="editrecipientCompany">Nom de l'entreprise</p>
                                <p id="editrecipientName">Nom et prénom</p>
                                <p id="editrecipientEmail">email@domaine.com</p>
                            </div>

                            <!-- Facture Info -->
                            <div class="text-right">
                                <!--<p id="factureCode">12345</p>-->
                                <p id="editfactureDate">01/01/2024</p>
                                <p id="editissuerName">{{ request.user.nom }}</p>
                            </div>
                        </div>

                        <!-- Product Details Table -->
                        <div class="overflow-x-auto">
                            <table class="w-full border-t border-b border-gray-300">
                                <thead>
                                <tr>
                                    <th class="p-2 text-left">Désignation & Référence</th>
                                    <th class="p-2 text-center">Prix Unitaire</th>
                                    <th class="p-2 text-center">Quantité</th>
                                    <th class="p-2 text-center">Total</th>
                                </tr>
                                </thead>
                                <tbody id="editproductDetails">
                                <!-- Product rows will be inserted here dynamically -->
                                </tbody>
                            </table>
                        </div>

                        <!-- Total Section -->
                        <div class="flex justify-end">
                            <div class="mt-4 w-1/3">
                                <div class="flex justify-between mt-2 font-semibold">
                                    <span>Total:</span>
                                    <span id="edittotalAmount" class="pr-2">0 DA</span>
                                </div>
                                <div class="flex justify-between mt-2 font-semibold">
                                    <span>TVA:</span>
                                    <span id="edittaxAmount" class="pr-2">0 DA</span>
                                </div>
                                <div class="flex justify-between mt-2 font-semibold">
                                    <span>Montant Total:</span>
                                    <span id="editamountDue" class="pr-2">0 DA</span>
                                </div>
                            </div>
                        </div>


                    </div>
                </div>

                <!-- Buttons -->
                <div class="flex justify-between items-center mt-4">
                    <button class="editgoToStep2 bg-gray-500 text-white px-4 py-2 rounded-lg">Retour</button>
                    <button id="editconfirmOrder" class="bg-green-500 text-white px-4 py-2 rounded-lg">Confirmer</button>
                </div>
            </div>

        </div>
"""